# Blog.py with simple SQL database

## [Live Link to Project on Replit](https://16d1ac62-a290-4617-a78f-abdb380673a2-00-m2q2tbltvitv.janeway.replit.dev/)

## Endpoints:

```shell
Endpoint               Methods    Rule                            
---------------------  ---------  --------------------------------
add_to_favorites       POST       /favorites/add                  
create_new_comment     POST       /new-comment/<int:post_id>      
create_new_entry       GET, POST  /new-post/                      
create_user            GET, POST  /create_user/                   
delete_comment         GET, POST  /delete-comment/<int:comment_id>
delete_entry           POST       /delete-post/<int:entry_id>     
delete_from_favorites  POST       /favorites/delete               
edit_entry             GET, POST  /edit-post/<int:entry_id>       
favorites              GET        /favorites/                     
filter_posts           GET        /filter/                        
homepage_view          GET        /                               
list_drafts            GET        /drafts/                        
login                  GET, POST  /login/                         
logout                 GET, POST  /logout/                        
movie_details          GET        /movie/<movie_id>               
movies_homepage        GET        /movies/                        
search                 GET        /search_movies                  
search_drafts          GET        /search_drafts/                 
search_posts           GET        /search/                        
static                 GET        /templates/<path:filename>      
user                   GET, POST  /user/  
```

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