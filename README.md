# mydotrepo ##

Welcome to mydotrepo! This repository contains my personal dotfiles for customizing my  linux i3wm desktop & development environment.

## Prerequisites

 --> Before using these dotfiles, ensure that you have [Git](https://git-scm.com) installed on your system.
 --> i3wm window manager should be installed.
 --> dotfiles will work well on arch and arch-based linux distros .....(not shure about debian and others)


## Installation

To install and configure the dotfiles on your system, follow these steps:

1. Clone the repository as a bare repository:

   ```bash
   git clone --bare https://github.com/thedistroyer17/mydotrepo.git $HOME/.mydotrepo
   ```

2. Define an alias called 'dotfiles' to interact with the bare repository:

   
   ```bash
    alias dotfiles='/usr/bin/git --git-dir=$HOME/.mydotrepo/ --work-tree=$HOME'
    ```

    Note: You may want to add this alias to your shell profile (e.g., .bashrc or .zshrc) for persistence.

3. Checkout the dotfiles:
  
    ```bash
     dotfiles checkout
    ```
     If you encounter conflicts , backup and remove the conflicting  files and rerun the checkout command.

4. Customize 
  Feel free to customize  any of the dotfiles to suit your needs. You can modify the configurations or add new ones according to your preferences. 

# Usage 
 To manage your dotfiles, you can use the 'dotfiles' alias we set up earlier. Here are a few example commands:
 
 1. To see the status of the changes:
 
    ```bash 
    dotfiles status 
    ```
 2. To ad changes to your dotfiles:
    ```bash
    dotfiles add <file1> <file2>
 3. To commit the changes:
    ```bash 
    dotfiles commit -m "updated Random__shit "
    ```
 4. To push changes to the respoitory:
    ```bash 
     dotfiles push 
    ```  

# Contact 
 If you have any questions or suggestiona regarding these dotfiles , please feel free to send pull requests and reach out to me at @--- darkxx6969@gmail.com

#### Good luck !!!

   


