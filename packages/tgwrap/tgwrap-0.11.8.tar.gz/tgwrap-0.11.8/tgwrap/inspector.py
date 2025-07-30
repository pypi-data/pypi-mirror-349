"""Verify a given Azure environment based on some verification config file"""

import os
import yaml
import requests
import json
import re

from typing import Tuple, Dict, List
from enum import Enum
from jinja2 import Template

from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError
from azure.mgmt.authorization import AuthorizationManagementClient

from .printer import Printer

class ResourceInspectionStatus(Enum):
    OK = "Successfully inspected the resource"
    NOK = "Resource does not have the right status"
    NEX = "Resource does not exist"
    NS = "Resource type is not supported"

class RoleAssignmentInspectionStatus(Enum):
    OK = "Successfully inspected the role assignments"
    NC = "Role assignments not checked"
    NOK = "(Some) role assignments missing"

class AzureInspector():
    _printer = None
    _subscription_id = None
    _domain = None
    _substack = None
    _stage = None
    _config = {}
    _credential = None
    _client = None
    _graph_token = None
    _mngt_token = None
    _role_definitions = {}
    _result = {}

    @property
    def printer(self):
        return self._printer

    @property
    def subscription_id(self):
        return self._subscription_id

    @property
    def domain(self):
        return self._domain

    @property
    def substack(self):
        return self._substack

    @property
    def stage(self):
        return self._stage

    @property
    def config(self):
        return self._config

    @property
    def credential(self):
        return self._credential

    @property
    def client(self):
        return self._client

    @property
    def graph_token(self):
        return self._graph_token

    @property
    def mngt_token(self):
        return self._mngt_token

    @property
    def role_definitions(self):
        return self._role_definitions

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    def __init__(self, subscription_id:str, domain:str, substack:str, stage:str, config_file:str, verbose:bool, managed_identity_client_id:str = None):
        self._printer = Printer(verbose)
        self._subscription_id = subscription_id
        self._domain = domain
        self._substack = substack
        self._stage = stage

        # load the config file
        self._config = self._load_config(config_file)

        # get a credential
        self._credential = DefaultAzureCredential(
            # if you are using a user-assigned identity, the client id must be specified here!
            managed_identity_client_id = managed_identity_client_id,
        )

        self._client = AuthorizationManagementClient(
            credential=self.credential,
            subscription_id=self.subscription_id,
        )

        # Retrieve all role definitions
        self.printer.verbose('Retrieve all role definitions')
        role_definitions_iter = self.client.role_definitions.list(
            scope=f'/subscriptions/{self.subscription_id}'
        )
        for rd in role_definitions_iter:
            self._role_definitions[rd.role_name.lower()] = rd.name

    def _get_value_from_dict(self, data:str, property:str) -> str:
        """Get a value from a dict with a string that indicates the hierarchy with a dot"""

        keys = property.split('.')
        value = data
        for key in keys:
            if value:
                value = value.get(key)

        return value

    def _load_config(self, config_file:str) -> Dict:
        with open(config_file, 'r') as file:
            try:
                data = yaml.safe_load(file)
                return data
            except yaml.YAMLError as exc:
                self.printer.error(f"Error loading YAML file: {exc}")
                return None

    def _load_yaml_template(self, template_file:str, inputs:Dict) -> Dict:
        with open(template_file, 'r') as file:
            try:
                template_content = file.read()
                template = Template(template_content)
                rendered_yaml = template.render(inputs)

                data = yaml.safe_load(rendered_yaml)
                return data
            except yaml.YAMLError as exc:
                self.printer.error(f"Error loading YAML template file: {exc}")
                return None

    def _invoke_api(self, url:str, token:str, method:str='get', data:Dict=None) -> Dict:
        """Invoke the Azure API"""

        self.printer.verbose(f'Invoke {method.upper()} on {url}')
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        resp = None
        try:
            if method.lower() == 'get':
                resp = requests.get(url, headers=headers)
            elif method.lower() == 'post':
                resp = requests.post(url, headers=headers, json=data)
            elif method.lower() == 'delete':
                resp = requests.delete(url, headers=headers)
            else:
                raise ValueError(f'Method {method} not recognised')

            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            self.printer.verbose(f'Error occurred:\n{e.response.text}')
            return None

    def inspect(self):
        try:
            self._graph_token = self.credential.get_token('https://graph.microsoft.com/.default').token
            self._mngt_token = self.credential.get_token('https://management.azure.com/.default').token
        except ClientAuthenticationError as e:
            self.printer.error(
                f'Could not retrieve an azure token, are you logged in?',
                print_line_before=True,
                print_line_after=True,
            )
            raise (e)

        self.result = {}

        try:
            # read the config
            location_code = self.config['location'].get('code', 'westeurope')
            location_full = self.config['location'].get('full', 'West Europe')
            resources = self.config.get('resources', [])
            groups = self.config.get('entra_id_groups', {})

            # read the map that determines how to test a particular resource type
            resource_types = self._load_yaml_template(
                template_file=os.path.join(os.path.dirname(__file__), 'inspector-resources-template.yml'),
                inputs={
                    'location_code': location_code,
                    'location_full': location_full,
                },
            )

            # first check the groups, this will also enrich the map with the IDs of the actual groups
            # build a list
            groups_to_verify = []
            for role, name in groups.items():
                groups_to_verify.append({
                    'identifier': name.format(
                        domain=self.domain,
                        substack=self.substack,
                        stage=self.stage,
                    ),
                    'type': 'entra_id_group',
                    'role': role,
                })
            # and verify
            groups = self.inspect_resources(
                resources=groups_to_verify,
                resource_types=resource_types,
                groups=groups,
            )

            # now inspect the resources
            self.inspect_resources(
                resources=resources,
                resource_types=resource_types,
                groups=groups,
            )

            return self.result
        finally:
            # ensure new messages are printed on a new line, as the progress indicator does not create a new line
            self.printer.normal('')

    def inspect_resources(self, resources:List, resource_types:Dict, groups:Dict) -> Dict:
        for resource in resources:
            self.printer.progress_indicator()

            # get some identifiers from the config and replace with real values
            identifier = resource['identifier'].format(
                subscription_id=self.subscription_id,
                domain=self.domain,
                substack=self.substack,
                stage=self.stage,
            )
            # it might be that we have an alternative id, as sometimes these are shortened because of length restrictions
            alternative_ids = []
            for id in resource.get('alternative_ids', []):
                alternative_ids.append(
                    id.format(
                        subscription_id=self.subscription_id,
                        domain=self.domain,
                        substack=self.substack,
                        stage=self.stage,
                    )
                )

            resource_group = resource.get('resource_group', '').format(
                domain=self.domain,
                substack=self.substack,
                stage=self.stage,
            )

            type = resource['type']
            self.result[identifier] = {
                "type": type,
            }
            this_result = self.result[identifier]

            self.printer.verbose(f'Inspect {identifier} ({resource_group})')

            # now we can start inspecting these
            if type in resource_types:
                resource_type = resource_types[type]
                url = resource_type['url'].format(
                    subscription_id=self.subscription_id,
                    resource_group=resource_group,
                    name=identifier,
                )

                # which token to use?
                graph_api = False
                if 'graph.microsoft.com' in url:
                    graph_api = True
                    token = self.graph_token
                elif 'management.azure.com' in url:
                    token = self.mngt_token
                else:
                    self.printer.error(f'Do not have token for url: {url}')
                    break

                resp = self._invoke_api(url=url, token=token)

                # if we don't get anything back, try alternative ids (if we have some)
                if (not resp or (graph_api and len(resp.get('value', [])) == 0)):
                    for id in alternative_ids:
                        resp = self._invoke_api(url=url, token=token)
                        url = resource_type['url'].format(
                            subscription_id=self.subscription_id,
                            resource_group=resource_group,
                            name=id,
                        )
                        resp = self._invoke_api(url=url, token=token)

                        # now check if we have something, we stop at first hit
                        if (not graph_api and resp) or (graph_api and len(resp.get('value', [])) > 0):
                            identifier = id
                            break

                if not resp or (graph_api and len(resp.get('value', [])) == 0):
                    status = ResourceInspectionStatus.NEX.name
                    if resource_group:
                        msg = f"Resource {identifier} (in {resource_group}) of type {type} not found"
                    else:
                        msg = f"Resource {identifier} of type {type} not found"
                    ra_status = RoleAssignmentInspectionStatus.NC.name
                    ra_msg = ''
                else:
                    self.printer.verbose(json.dumps(resp, indent=2))

                    status = ResourceInspectionStatus.OK.name # we're innocent until proven otherwise
                    msg = ""
                    for property, expected_value in resource_type['properties'].items():
                        property_value = self._get_value_from_dict(data=resp, property=property)
                        if isinstance(property_value, str) and not re.match(expected_value, property_value):
                            status = ResourceInspectionStatus.NOK.name
                            msg = msg + f"Property {property} has value {property_value}, expected regex {expected_value}"
                        elif isinstance(property_value, bool) and not property_value:
                            status = ResourceInspectionStatus.NOK.name
                            msg = msg + f"Property {property} has value {property_value}, expected boolean {expected_value}"

                    # set the default status that we haven't check the role assignments
                    ra_status = RoleAssignmentInspectionStatus.NC.name
                    ra_msg = 'Role assignments not checked'

                    # if this is an entra id group, we store the object id
                    if type == 'entra_id_group':
                        role = resource['role']
                        id = resp['value'][0]['id']
                        groups[role] = {
                            'id': id,
                            'name': identifier,
                        }
                    elif 'role_assignments' in resource:

                        ra_status, ra_msg = self.check_role_assignments(
                            resource=resource,
                            groups=groups,
                            url=url,
                        )

                    if not msg:
                        if resource_group:
                            msg = f"Resource {identifier} (in {resource_group}) of type {type} OK"
                        else:
                            msg = f"Resource {identifier} of type {type} OK"
                    if not ra_msg and ra_status == RoleAssignmentInspectionStatus.OK.name:
                        ra_msg = f"Role Assignments for {identifier} (in {resource_group}) of type {type} are OK"

                this_result["inspect_status_code"] = status
                this_result["inspect_status"] = ResourceInspectionStatus[status].value
                this_result["inspect_message"] = msg

                if not type == 'entra_id_group':
                    this_result["rbac_assignment_status_code"] = ra_status
                    this_result["rbac_assignment_status"] = RoleAssignmentInspectionStatus[ra_status].value
                    if ra_msg:
                        this_result["rbac_assignment_message"] = ra_msg
            else:
                self.printer.error(f'\nResource type {type} is not configured in tgwrap!')
                this_result["inspect_status_code"] = ResourceInspectionStatus.NS.name
                this_result["inspect_status"] = ResourceInspectionStatus.NS.value
                this_result["inspect_message"] = f'Resource type {type} is not supported'

        # the groups dict is updated with the IDs of the actual groups
        return groups
    
    def check_role_assignments(self, resource:Dict, groups:Dict, url:str):

        status = RoleAssignmentInspectionStatus.NC.name
        msg = ''

        # extract the scope from the url
        base_url=url.split('?')[0].rstrip('/')
        scope = base_url.replace('https://management.azure.com', '')
        self.printer.verbose('\nGet permissions over scope: ', scope)

        # first get the role assignments for each (unique) principals
        principals = set()
        for ra in resource['role_assignments']:
            principals.update(ra.keys())
        
        principals = list(principals)
        principal_assignments = {} # here we collect all assignments for this scope per principal
        for p in principals:
            principal_assignments[p] = []

            if not p in groups:
                self.printer.error(f'\nCannot find the group {p} in groups: {groups}')
                continue
            elif not 'id' in groups[p]:
                self.printer.error(f'\nCannot find the id for group {p}: {groups[p]}')
                continue

            principal_id = groups[p]['id']
            assignments = self.client.role_assignments.list_for_scope(
                scope=scope,
                filter=f"principalId eq '{principal_id}'",
            )

            # get the IDs of all roles assigned for the given scope
            for a in assignments:
                principal_assignments[p].append(a.role_definition_id.split('/')[-1]) # we only want the guid of the role definition

        # assume the role assignments will be fine
        status = RoleAssignmentInspectionStatus.OK.name
        for role in resource['role_assignments']:
            principal = list(role.keys())[0]
            role = list(role.values())[0]

            if role.lower() not in self.role_definitions:
                raise ValueError(f"Role: '{role}' is not found.")

            if (self.role_definitions[role.lower()] not in principal_assignments[principal]):
                status = RoleAssignmentInspectionStatus.NOK.name
                msg = msg + f'Principal {principal} has NOT role {role} assigned; '

        return status, msg
