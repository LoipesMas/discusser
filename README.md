# discusser
Simple discussion service api

Made using django and django rest framework

## Models
Post:
- `date`: date of creation
- `content`: text content of the post
- `author`: author of the post
- `get_likes()`: returns the count of likes on this post

Like:
- `user`: user who liked
- `post`: post which was liked

## API
- `/api/posts/` for post list and creation
- `/api/posts/<n>/` for detail about post with id `n` (for retrieval, updating and deleting)
- `/api/likes/` for creating a like
