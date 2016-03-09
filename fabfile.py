from fabric.api import local

def update():
    local('git checkout master')
    local('git pull origin develop')

def deploy():
    local('git add .')
    local('git commit -m "deploy"')
    local('git push openshift HEAD:master')
