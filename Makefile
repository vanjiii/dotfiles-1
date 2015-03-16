ALL   := bash tmux X git mercurial vim ipython ranger zsh systemd

update:
	git pull
	git submodule sync
	git submodule foreach "git checkout master; git pull origin master; echo"
	$(MAKE) install

install: $(ALL:%=install-%)

install-X:
	ln -fs `pwd`/Xmodmap ~/.Xmodmap
	ln -fs `pwd`/xinitrc ~/.xinitrc
	ln -fs `pwd`/Xdefaults ~/.Xdefaults
	ln -fs `pwd`/Xresources ~/.Xresources

install-bash:
	ln -fs `pwd`/sh/rc ~/.bashrc
	ln -fs `pwd`/bash/profile ~/.bash_profile

install-tmux:
	ln -fs `pwd`/tmux/tmux.conf ~/.tmux.conf

install-git:
	ln -fs `pwd`/gitconfig ~/.gitconfig

install-vim:
	[[ -d ~/.vim ]] || ( git clone git@github.com:Vladimiroff/Vimfiles.git ~/.vim && cd ~/.vim && make install )
	ln -fs `pwd`/ctags ~/.ctags

install-ipython:
	[[ -d ~/.config/ipython ]] || mkdir -p ~/.config/ipython/profile_default
	ln -fs `pwd`/ipython/profile_default/ipython_config.py ~/.config/ipython/profile_default/ipython_config.py

install-ranger:
	mkdir -p ~/.config/ranger/
	ln -fs `pwd`/ranger/* ~/.config/ranger/

install-zsh:
	ln -fs `pwd`/sh/rc ~/.zshrc

install-mercurial:
	ln -fs `pwd`/hgrc ~/.hgrc

install-systemd:
	cp `pwd`/systemd/user/* ~/.config/systemd/user/
