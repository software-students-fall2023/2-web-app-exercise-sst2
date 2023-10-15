// fetch posts
const fetchPosts = async () => {
    const res = await fetch('/feed-posts', {
        method: "GET"
    })
    const postList = await res.json()

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
    commentCount.textContent = `${comments.length} comment${comments.length === 1 ? '' : 's'}`

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
const postsInit = async () => {
    const postListDiv = document.getElementById('posts-list-div')
    
    const postList = await fetchPosts()
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
