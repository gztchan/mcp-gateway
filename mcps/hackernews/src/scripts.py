fetch_more_stories_script = """() => {
    document.querySelector(".hn-items-more")?.click()
}
"""

simple_stories_script = """() => {
    const simple_stories = [];
    const hn_content = document.querySelector("#hn_content");
    const items = hn_content.querySelectorAll(".hn-items > .hn-item");
    const more_button = document.querySelector(".hn-items-more")

    for (let i = 0; i < items.length; i++) {
        const item = items[i]

        const author_element = item.querySelector(".hn-item-user")
        let author = null
        if (author_element) {
            author = {
                "id": author_element.getAttribute("data-username"),
                "profile_url": author_element.getAttribute("href"),
                "username": author_element.getAttribute("data-username"),
            }
        }

        const id = item.getAttribute('id');
        simple_stories.push({
            "id": id,
            "title": item.querySelector(".hn-item-title").innerText,
            "resource": item.querySelector(".hn-item-domain")?.getAttribute("href"),
            "url": item.querySelector(".hn-item-oldness")?.getAttribute("href"),
            "created_at": item.querySelector(".hn-item-age")?.getAttribute("title")?.split(" ")[0],
            "points": item.querySelector(".hn-item-score")?.innerText?.replace(" points", ""),
            "comments": item.querySelector(".hn-item-oldness")?.innerText?.replace(" comments", ""),
            "author": author,
        })
    }

    return simple_stories
}
"""

story_script = """() => {
    const title_element = document.querySelector(".hn-story-title");
    const comments_elements = document.querySelectorAll(".hn-comments > .hn-comment");
    const story_info = document.querySelector(".hn-story-info");
    const story_author_element = story_info.querySelector(".hn-story-info-user.hn-user-link");

    const story_author = {
        "id": story_author_element?.getAttribute("data-username"),
        "profile_url": story_author_element?.getAttribute("href"),
        "username": story_author_element?.getAttribute("data-username"),
    }

    const comments = [];
    for (let i = 0; i < comments_elements.length; i++) {
        const comment_element = comments_elements[i];
        const info = comment_element.querySelector(".hn-comment-info");
        const author_element = info.querySelector(".hn-comment-info-user.hn-user-link");

        const author = {
            "id": author_element?.getAttribute("data-username"),
            "profile_url": author_element?.getAttribute("href"),
            "username": author_element?.getAttribute("data-username"),
        }

        comments.push({
            "id": comment_element?.getAttribute("id"),
            "content": comment_element?.querySelector(".hn-comment-text").innerHTML,
            "author": author,
            "created_at": comment_element?.querySelector(".hn-story-info-age")?.getAttribute("title").split(" ")[0],
        })
    }

    return {
        "url": location.href,
        "title": title_element.innerText,
        "resource": title_element?.getAttribute("href"),
        "comments": comments,
        "author": story_author,
    }
}"""