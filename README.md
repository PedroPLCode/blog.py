# Blog.py with simple SQL database

## Endpoints:

Endpoint          Methods    Rule                      
----------------  ---------  --------------------------
create_new_entry  GET, POST  /new-post/                
edit_entry        GET, POST  /edit-post/<int:entry_id> 
homepage_view     GET        /                         
static            GET        /templates/<path:filename>

## Data Base setup:

init db:
```shell
flask db init
```

prep db migration:
```shell
flask db migrate
```

migrate db:
```shell
flask db upgrade
```