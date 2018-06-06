#!/usr/bin/python
import jenkins
from ansible.module_utils.basic import *

create_credential_groovy = u"""
import jenkins.*;
import jenkins.model.*;
import hudson.*;
import hudson.model.*;

import com.cloudbees.plugins.credentials.domains.Domain;
import com.cloudbees.plugins.credentials.CredentialsScope;

domain = Domain.global()
store = Jenkins.instance.getExtensionList(
  'com.cloudbees.plugins.credentials.SystemCredentialsProvider'
)[0].getStore()

credsNew = new {userPrivateKey}(
  CredentialsScope.GLOBAL, '{credentialsId}',
  '{userName}',
  new {privateKeySource}('''{sshKeyText}'''),
  '{sshKeyPassphrase}',
  '{description}'
)

creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
  {userPrivateKey}.class, Jenkins.instance
);
updated = false;

for (credsCurr in creds) {{
  // Comparison does not compare passwords but identity.
  if (credsNew == credsCurr) {{
    store.removeCredentials(domain, credsCurr);
    ret = store.addCredentials(domain, credsNew)
    updated = true;
    println('OVERWRITTEN');
    break;
  }}
}}

if (!updated) {{
  ret = store.addCredentials(domain, credsNew)
  if (ret) {{
    println('CREATED');
  }} else {{
    println('FAILED');
  }}
}}
"""  # noqa

def _render_create_creds_groovy(kwargs):
  return create_credential_groovy.format(
    credentialsId=kwargs['credentialsId'],
    userName=kwargs['userName'],
    description=kwargs['description'],
    userPrivateKey=kwargs['userPrivateKey'],
    privateKeySource=kwargs['privateKeySource'],
    sshKeyText=kwargs['sshKeyText'],
    sshKeyPassphrase=kwargs['sshKeyPassphrase']
  )

def _jenkins_cli(jenkins_url=None, username=None, password=None, **kwargs):
  result = {
    'cmd': '{}'.format(jenkins_url),
    'changed': False,
    'failed': True,
    'msg': None,
    'rc': 1
  }

  server = jenkins.Jenkins(jenkins_url, username, password)

  groovy = _render_create_creds_groovy(**kwargs)
  result['cmd'] += ' {}'.format(groovy)

  try:
    output = server.run_script(groovy)
    if 'Error' in output or 'Exception' in output:
      result['msg'] = output
      return result

  except jenkins.JenkinsException as e:
    result['msg'] = e.message
    return result

  result['jenkins_cli'] = output
  result['changed'] = True
  result['failed'] = False
  result['rc'] = 0

  return result


if __name__ == '__main__':
  global module
  module = AnsibleModule(
    argument_spec={
      'jenkins_url': {'required': True},
      'username': {'required': True},
      'password': {'required': True},
      'kwargs': {'required': False, 'type': 'dict'},
    },
    supports_check_mode=False
  )
  module.exit_json(**_jenkins_cli(**module.params))
