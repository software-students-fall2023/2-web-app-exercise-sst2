// fetch posts
const fetchPosts = async () => {
    const res = await fetch('/feed-posts', {
        method: "GET"
    })
    const postList = await res.json()

    return postList
}

// vote on post
const votePost = async (postEle, good) => {
    console.log(postEle);
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
    ele.className = classname
    return ele
}

// Post component
const Post = ({_id, title, content, comments, user}) => {
    const postContainer = eleWithClass('div', 'post-container')
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
    const numComments = comments?.length ?? 0
    commentCount.textContent = `${numComments} comment${numComments === 1 ? '' : 's'}`
    const postVoting = eleWithClass('div', 'post-voting')
    const postRating = eleWithClass('span', 'post-rating')
    postRating.textContent = 12
    const voteGood = eleWithClass('button', 'post-vote-btn vote-good')
    const voteBad = eleWithClass('button', 'post-vote-btn vote-bad')
    const voteGoodIcon = eleWithClass('span', 'vote-btn-icon')
    const voteBadIcon = eleWithClass('span', 'vote-btn-icon')
    voteGoodIcon.textContent = '👍'
    voteBadIcon.textContent = '👎'
    voteGood.addEventListener('click', (e) => { e.preventDefault(); votePost(postItem, true) })
    voteBad.addEventListener('click', (e) => { e.preventDefault(); votePost(postItem, false) })


    // build and append
    const postDoc = document.createDocumentFragment()
    buildDocument(postDoc, [
        { n: postContainer, c: [
            { n: postItem, c: [
                { n: postTop, c: [
                    { n: postTitle },
                    { n: postAuthor, c: [
                        { n: authorName },
                    ]},
                ]},
                { n: postContent },
                { n: eleWithClass('div', 'post-bottom-placeholder')}
            ]},
            { n: postBottom, c: [
                { n: commentCount },
                { n: postVoting, c: [
                    { n: voteGood, c: [
                        {n: voteGoodIcon },
                    ]},
                    { n: postRating },
                    { n: voteBad, c: [
                        {n: voteBadIcon },
                    ]},
                ]},
            ]},
        ]},
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
