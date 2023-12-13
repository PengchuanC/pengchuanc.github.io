
echo "打包hugo"
hugo -d docs

echo "输入commit的内容"

read message

git add .
git commit -a -m "$message"
git push
