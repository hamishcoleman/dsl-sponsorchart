It would be nice if github had a simple API that allowed you to fetch the
same information that regular users see when they begin to sponsor an org.

This repository contains a small tool for providing this data.

Specifically:

```
44% towards $2,300 per month goal
xxxxxxxxxxxxxxxxxx----------------------
xyzzy and 10 others sponsor this goal
```

To draw this barchart, we need:
- goal
- current amount

There is a github API via graphql for this data, but it requires
authentication - even though it is clearly public data.
