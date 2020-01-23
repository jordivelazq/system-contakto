from fabric.api import local

def deploy():
  local('git rev-parse HEAD > SHA1.txt')
  local('docker build -t garciadiazjaime/admin-contakto .')
  local('docker push garciadiazjaime/admin-contakto')
  local('echo "docker pull garciadiazjaime/admin-contakto"')
