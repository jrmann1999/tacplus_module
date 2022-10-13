#!/usr/bin/env python3

# Copyright: (c) 2022, Jeremy Mann <jeremy.richard.mann@gmail.com>
# GNU General Public License v3.0+ (see copying or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
---
module: tacplus_authorize

short_description: A modules to test TACACS authorization (with a command)

version_added: "1.0.0"

description: A module used to test TACACS authorization, with a command, against Cisco ISE servers

options:
    tac_username:
        description: Username to authorize
        required: true
        type: str
    tac_server:
        description: Server IP to test this agains
        required: true
        type: str
    tac_secret:
        description: The secret to encrypt TACACS communication with the server
        required: true
        type: str
    tac_command:
        description: The command to authorize on the server
        required: true
        type:str

author:
    - Jeremy Mann (@jrmann1999)
'''

EXAMPLES = r'''
# Authorization test with command
- name: Authorization Test (show version)
      tacplus_authorize:
        tac_username: 'USER'
        tac_server: 'IP'
        tac_secret: "{{ credentials.tacsecret }}"
        tac_command: 'show version'
'''

RETURN = r'''
Returns a message with success or failure
'''

from ansible.module_utils.basic import AnsibleModule
from tacacs_plus.client import TACACSClient

def run_module():
    module_args = dict(
        tac_username = dict(type='str', required=True),
        tac_server=dict(type='str', required=True), 
        tac_secret = dict(type='str', required=True),
        tac_command = dict(type='str', required=False)
    )

    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleModule(
        supports_check_mode=False,
        argument_spec=module_args
    )

    tac_username = module.params['tac_username']
    tac_server = module.params['tac_server']
    tac_secret = module.params['tac_secret']
    tac_command = module.params['tac_command'].split(' ')
    cmd = 'cmd=' + tac_command[0]
    args = 'cmdarg = ' + tac_command[1]

    cli = TACACSClient(tac_server, 49, tac_secret, timeout=10)
    authorize = cli.authorize(tac_username, arguments=[b'service=shell', bytes(cmd, 'utf-8'), bytes(args, 'utf-8')] )
    if authorize.valid:
        result['message'] = "Success!"
    else:
        result['message'] = 'Failure!'
        return result

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()