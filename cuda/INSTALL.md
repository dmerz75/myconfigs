# CUDA/SOP
<!-- https://aspratyush.wordpress.com/2012/05/06/install-nvidia-cuda-on-centos-6/ -->

Install Nvidia Driver and CUDA Toolkit on CentOS 6
( Update: have posted a MUCH simpler method of driver install. Steps for CUDA toolkit install have to be followed as given in this post, i.e. , bulleted step # 10 – 19 )

Although the topic has been addressed succinctly in a CentOS forum post, there are certain things like plymouth configuration post Nvidia driver install, etc. which I felt needed to be jotted down for reference. So, here we go describing the Nvidia CUDA toolkit installation on a CentOS system:

Download the appropriate toolkit, driver and SDK from Nvidia’s website.
RHEL, and its derivatives come with the open source Nvidia driver called nouveau. Before installing Nvidia drivers, we need to ensure nouveau drivers dont get loaded. For this, append the following in the line starting with 'kernel' in the file /etc/boot/grub.conf:

rdblacklist=nouveau nouveau.modeset=0

Install the Development Tools and Development Libraries group packages, and a few extra packages listed below:

sudo yum groupinstall ‘Development Tools’ ‘Development Libraries’

sudo yum install kernel-devel gcc-c++ freeglut freeglut-devel libX11-devel mesa-libGLU-devel libXmu-devel libXi-devel gcc* compat-gcc* compat-glibc* compat-lib*

Restart the system. Upon restart, you'll see that the resolution of the display would have gone for a toss. Thats due to blacklisting the nouveau driver, and is a sign that we are on track! Open terminal and type the following to goto non-GUI mode (called, runlevel 3):

sudo init 3

Above command takes us to text mode. Change directory to /usr/src/kernels/ and note down the complete path of the kernel folder present. In our scenario, it shows up as:

/usr/src/kernels/2.6.32-220.13.1.el6.x86_64/

Change directory to the folder containing the downloaded files from Nvidia’s website (say ~/Downloads). Mark the 3 downloaded files as executables:

cd ~/Downloads

chmod a+x NV*; chmod a+x cuda*; chmod a+x gpu*

Now finally, we are ready to run the installer. First is the Nvidia Driver install :

sudo sh NVIDIA-Linux-x86_64-295.20.run –kernel-source-path=/usr/src/kernels/2.6.32-220.13.1.el6.x86_64/

NOTE : there’s a double minus sign before the word kernel above. During the above install, accept the licence agreement shown. Reboot upon completion:

sudo reboot

You'll notice that the GUI resolution is back to normal, indicating successful Nvidia driver install. Now, cudatoolkit has to be installed.
Open terminal and change directory to ~/Downloads. Run the cudatoolkit*.run file:

sudo sh cudatoolkit_4.0.17_linux_64_rhel6.0.run

During the install, you'll be asked to supply installation path. Enter the default path itself (/usr/local/cuda).
Once completed, few more steps are needed, like adding /usr/local/cuda to default path environment variable, etc. :

sudo nano /etc/ld.so.conf.d/cuda.conf

Add the following lines to the above created file :

/usr/local/cuda/lib64
/usr/local/cuda/lib

Save the above file by pressing Ctrl+x, followed by ‘y’ and pressing Enter. Now run:

sudo ldconfig

For adding cuda install path to enviroment path variable, edit ~/.bash_profile file using a text editor (say, nano ~/.bash_profile) :

export CUDA_INSTALL_PATH=/usr/local/cuda
export PATH=($PATH: /usr/local/cuda/bin)
export LD_LIBRARY_PATH=/usr/local/cuda/lib64
export PATH=($PATH: /usr/local/cuda/lib)

Finally, gpucomputingsdk needs to be installed. For that :

sh gpucomputingsdk_4.0.17_linux.run

During the install , you'll be asked for install path. Keep in mind that the sdk can take around 400-500MB. Say, we install it to ~/Documents/NVIDIA_GPU_Computing_SDK.
Once done, we need to compile the files in the SDK:

cd ~/Documents/NVIDIA_GPU_Computing_SDK/C/

make

To check whether everything is working fine, we’ll run the deviceQuery file, provided by the SDK just installed:

cd ~/Documents/NVIDIA_GPU_Computing_SDK/C/bin/linux/release/

./deviceQuery
