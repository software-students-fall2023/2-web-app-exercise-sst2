// fetch posts
const fetchPosts = async () => {
    const res = await fetch('/feed-posts', {
        method: "GET"
    })
    const postList = await res.json()

    return postList
}

// helper function to build document
// children = [{n: node, c: [node]}]
const buildDocument = (parent, children) => {
    if (children !== undefined) {
        for (const {n, c} of children) {
            parent.appendChild(n)
            buildDocument(n, c)
        }
    }
}

// helper function to create element with class name
const eleWithClass = (tag, classname) => {
    const ele = document.createElement(tag)
    ele.classList.add(classname)
    return ele
}

// Post component
const Post = ({_id, title, content, comments, user}) => {
    const postItem = eleWithClass('a', 'post-item')
    postItem.href = `/post/${_id.$oid}`

    // top of post (title, author)
    const postTop = eleWithClass('div', 'post-top')
    const postTitle = eleWithClass('h2', 'post-title')
    postTitle.textContent = title
    const postAuthor = eleWithClass('a', 'post-author')
    postAuthor.href = `/profile/${user}`
    postAuthor.textContent = 'by '
    const authorName = eleWithClass('span', 'post-author-name')
    authorName.textContent = user

    // post content
    const postContent = eleWithClass('p', 'post-content')
    postContent.textContent = content

    // post bottom (comments, rating?)
    const postBottom = eleWithClass('div', 'post-bottom')
    const commentCount = eleWithClass('span', 'post-comment-count')
    commentCount.textContent = `${comments.length} comment${comments.length === 1 ? '' : 's'}`

    // build and append
    const postDoc = document.createDocumentFragment()
    buildDocument(postDoc, [
        { n: postItem, c: [
            { n: postTop, c: [
                { n: postTitle },
                { n: postAuthor, c: [
                    { n: authorName }
                ]}
            ]},
            { n: postContent },
            { n: postBottom, c: [
                { n: commentCount }
            ]},
        ]}
    ])

    return postDoc
}

// post separator (<hr>)
const PostSep = () => {
    const postSepHR = document.createElement('hr')
    postSepHR.classList.add('post-sep')
    return postSepHR
}

// init post list
const postsInit = async () => {
    const postListDoc = document.createDocumentFragment()
    
    const postList = await fetchPosts()
    for (const post of postList) {
        postListDoc.appendChild(Post(post))
        postListDoc.appendChild(PostSep())
    }

    const postListDiv = document.getElementById('posts-list-div')
    postListDiv.appendChild(postListDoc)
}

// init when ready
if (document.readyState !== 'loading') {
    postsInit()
} else {
    window.addEventListener('DOMContentLoaded', () => {
        postsInit()
    })
}
