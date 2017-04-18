EXAMPLES_LINK="https://imperiallondon-my.sharepoint.com/personal/ajaver_ic_ac_uk/_layouts/15/guestaccess.aspx?guestaccesstoken=ldZ18fLY%2bzlu7XuO9mbKVdyiKoH4naiesqiLXWU4vGQ%3d&docid=0cec4e52f4ccf4d5b8bb3a737020fc12f&rev=1"
EXAMPLES_DIR="~/tierpsy-tracker/tests/data/"

curl -L $EXAMPLES_LINK -o test_data.zip
rm -rf $EXAMPLES_DIR || : 
mkdir $EXAMPLES_DIR
unzip test_data.zip -d $EXAMPLES_DIR
rm test_data.zip