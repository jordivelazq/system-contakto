from fabric.api import local

def deploy():
  local('docker build -t garciadiazjaime/admin-contakto .')
  local('docker push garciadiazjaime/admin-contakto')
  local('echo "docker pull garciadiazjaime/admin-contakto"')
