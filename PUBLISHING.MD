## PUBLISHING

1 - Declare new version

```sh
poetry version <new_version>
```

2 - Commit version change

3 - Create a tag with new version

```sh
git tag <new_version>
```

4 - Publish
```
git push
git push --tags
```

5 - Pipeline will trigger automatically.
