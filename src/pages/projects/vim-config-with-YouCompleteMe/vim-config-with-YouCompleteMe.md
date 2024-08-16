date:          2024-08-16
categories:    tech|how-to

_August 16, 2024_

## Vim and YouCompleteMe: A Love Story

I made learning vim a priority when I first got into linux, and eventually got to the point where I wrote an entire 
api on MacVim (check out my old [neovim config repo](https://github.com/andybp85/nvim) for some insane nerdery). I've 
been using Webstorm for work for years, and so I got this site started using PyCharm. It's a great IDE, but I miss 
vim, so I decided to get vim set up to use for this site again.

My vim config and a summary of the steps here can be found in [this gist](https://gist.github.com/andybp85/e5075c69d45c6d8d012ea89199935ea6)

### Goals
* [YouCompleteMe](https://github.com/ycm-core/YouCompleteMe) - This is still the best completion enginer I've ever
used. It's kind of a pain to get setup, so that's why I'm writing this summary of what I did.
* [MacVim](https://macvim.org/) - I want this working in a GUI (I use Macbook Pros).
* Recreate all the features I need from PyCharm - This will be a WIP, so check back for updates.

### Guide
I had vim installed from source already, but it turned out I needed python support for YCM.

#### Python
I use [pyenv](https://github.com/pyenv/pyenv). I also installed vim and YCM in a virtualenv, which I think I've done 
before with no issues... so we shall see if that bites me in the future.

When I first tried to install YCM, I got this error on starting vim:

    symbol not found in flat namespace '_PyByteArray_Type'

Turns out YCM needs python with shared lib support, so I reinstalled the latest version with `--enable-framework`:

```zsh
> export PYTHON_CONFIGURE_OPTS="--enable-framework"
> arch --arm64 pyenv install  3.12.3
> pyenv global 3.12.3
```

#### Vim from source
This was easy... I think. I forget if I had to jump through any hoops to get it to compile in the first place, but I 
don't think so. I cloned the [github repo](https://github.com/vim/vim) and then:

```zsh
> python -m venv penv
> source penv/bin/activate
> ./configure --with-features=huge \
    --enable-multibyte \
    --enable-gtk3-check \
    --with-python3-command=python \
    --enable-python3interp=yes  
> sudo make install
```

I had already copied my .vimrc into the right place and installed [vim-plug](https://github.com/junegunn/vim-plug), so
the next step was just starting vim and running `:PlugInstall`

#### YouCompleteMe
This is also way simpler these days; when I first used it years ago I had to figure out how to get the c compiler to
use the Boost lib. I made sure I had the penv activated, then installed some deps it complained about:

    ::zsh
    > brew install cmake go

and then ran the install:

    ::zsh
    > python install.py --all

#### MacVim
Obviously the install here is easy, but I use the zsh (and the wonderful [iTerm2](https://iterm2.com/) which I'll 
have to write up a post on someday) and I want to be able to open files in MacVim easily. So I added this to my 
`.zprofile` (I use [zpresto](https://github.com/sorin-ionescu/prezto)):

    ::zsh
    alias mvim="open -a MacVim.app $1"

### Ta-da!
Everything works! I'm sure I'll be adding way more customizations and functionality to vim going forward, so check 
back at some point and see!

<div>
    <img alt="vim with monokai pro theme and YCM" height="474" width="600" src="/images/vim-YCM.webp" />
</div>
