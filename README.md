# some-application

## Application overview

* A user can create and login to a _user-account_.
* A _user-account_ consists of the following:
  * An _account-page_, which displays their _account-header_ and _post-pools_.
  * An _account-header_, which displays the following:
    * A unique _user-id_.
    * An optional _nickname_.
    * _Profile picture_.
    * Link to post and message history.
    * Link to _account-page_ of the user.
  * Zero or more _post-pools_.
  * _User-settings_, which contains various settings for _user_account_. 
*  A user user who doesn't have an account, or who is not logged in, can:
   * Browse, search and view _post-pools_, and the _posts_ and _chats_ they contain.
   * View _account-headers_ of other users.
   * View _account-pages_ of other users. 
* When a user is logged in, they can additionally:
  * Create new _post-pools_ for their own _user-account_.
  * Create _posts_ within their own _post-pools_ or other _post-pools_ for which they have _permission_ to create posts for.
  * Post messages in the _chats_ of various _posts_.
  * Edit their _user-settings_ and _account-page_.

## A post-pool
A post-pool is an ordered list of post-chat pairs. A post is some multimedia composition, consisting of a headline, 
zero or more "chunks" of text and zero or more pictures. Each post is paired with a chat, in which users can comment and discuss the related post.
