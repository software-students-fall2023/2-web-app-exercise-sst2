const dummypost = {
    "_id": {
        "$oid": "6529dee0699948aacd3a1e4c"
    },
    "title": "What is this you ask?",
    "content": "Well of course this is a post. This is a post to test posts and this is the content of the post. Therefore the post content is the content of the post of course.",
    "comments": [
        {
            "user": "firstCommenter",
            "comment": "I am the first comment!"
        },
        {
            "user": "secondCommenter",
            "comment": "I am the second Comment!"
        }
    ],
    "user": "Silver1793"
}

// fetch posts
const fetchPosts = () => {
    const postList = []
    for (let i = 0; i < 6; i += 1) {
        postList.push(dummypost)
    }
    return postList
}

// Post component
const Post = ({_id, title, content, comments, user}) => {
    const postItem = document.createElement('a')
    postItem.href = `/post/${_id.$oid}`
    postItem.classList.add('post-item')

    // top of post (title, author)
    const postTop = document.createElement('div')
    postTop.classList.add('post-top')

    const postTitle = document.createElement('h2')
    postTitle.classList.add('post-title')
    postTitle.textContent = title

    const postAuthor = document.createElement('a')
    postAuthor.classList.add('post-author')
    postAuthor.href = `/profile/${user}`
    postAuthor.textContent = 'by '

    const authorName = document.createElement('span')
    authorName.classList.add('post-author-name')
    authorName.textContent = user
    
    postAuthor.appendChild(authorName)
    postTop.appendChild(postTitle)
    postTop.appendChild(postAuthor)
    postItem.appendChild(postTop)

    // post content
    const postContent = document.createElement('p')
    postContent.classList.add('post-content')
    postContent.textContent = content
    postItem.appendChild(postContent)

    // post bottom (comments, rating?)
    const postBottom = document.createElement('div')
    postBottom.classList.add('post-bottom')

    const commentCount = document.createElement('span')
    commentCount.classList.add('post-comment-count')
    commentCount.textContent = `${comments.length} comments`

    postBottom.appendChild(commentCount)
    postItem.appendChild(postBottom)

    return postItem
}

// post separator (<hr>)
const PostSep = () => {
    const postSepHR = document.createElement('hr')
    postSepHR.classList.add('post-sep')
    return postSepHR
}

// init post list
const postsInit = () => {
    const postListDiv = document.getElementById('posts-list-div')
    
    const postList = fetchPosts()
    for (const post of postList) {
        postListDiv.appendChild(Post(post))
        postListDiv.appendChild(PostSep())
    }
}

// init when ready
if (document.readyState !== 'loading') {
    postsInit()
} else {
    window.addEventListener('DOMContentLoaded', () => {
        postsInit()
    })
}
