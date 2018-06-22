#!/usr/bin/python
import jenkins
from ansible.module_utils.basic import *

#http://code.activestate.com/recipes/576710-multi-regex-single-pass-replace-of-multiple-regexe/
class MultiRegex(object):
  flags = re.MULTILINE
  regexes = ()

  def __init__(self):
    '''
    compile a disjunction of regexes, in order
    '''
    self._regex = re.compile("|".join(self.regexes), self.flags)

  def sub(self, s):
    return self._regex.sub(self._sub, s)

  def _sub(self, mo):
    '''
    determine which partial regex matched, and dispatch on self accordingly
    '''
    for k, v in mo.groupdict().iteritems():
      if v:
        sub = getattr(self, k)
        if callable(sub):
          return sub(mo)
        return sub
    raise AttributeError, \
      'nothing captured, matching sub-regex could not be identified'


class ParenthesesRegex(MultiRegex):
  regexes = (
    r'(?P<left>\s+{$)',
    r'(?P<right>^\s*})'
  )

  left = lambda self, mo: mo.group() + '{'
  right = lambda self, mo: mo.group() + '}'

def _render_create_creds_groovy(kwargs):
  with open(kwargs['groovyScript'], 'r') as myfile:
    groovyScriptText = myfile.read()

  create_credential_groovy = ParenthesesRegex().sub(groovyScriptText)

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
