# set up the default terminal
ENV["TERM"]="linux"

Vagrant.configure("2") do |config|
  
  # set the image for the vagrant box
  config.vm.box = "ubuntu/focal64"

  # sεt the static IP for the vagrant box
  config.vm.network "private_network", ip: "192.168.50.4"
  
  # configure the parameters for VirtualBox provider
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 4
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end
end
