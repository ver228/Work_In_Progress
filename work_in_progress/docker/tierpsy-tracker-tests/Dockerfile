FROM tierpsy-tracker

RUN yum -y install unzip
RUN curl -L "https://imperiallondon-my.sharepoint.com/personal/ajaver_ic_ac_uk/_layouts/15/guestaccess.aspx?guestaccesstoken=ldZ18fLY%2bzlu7XuO9mbKVdyiKoH4naiesqiLXWU4vGQ%3d&docid=0cec4e52f4ccf4d5b8bb3a737020fc12f&rev=1" -o ~/test_data.zip
RUN mkdir ~/tierpsy-tracker/tests/data && \
	unzip ~/test_data.zip -d ~/tierpsy-tracker/tests/data && \
	rm ~/test_data.zip

CMD cd ~/tierpsy-tracker && \
	git checkout HEAD && \
	source ~/.bashrc && \
	python ./tests/run_tests.py 