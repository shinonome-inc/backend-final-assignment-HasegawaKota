const getCookie = name => {
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) {
                return decodeURIComponent(value);
            }
        }
    }
};

const csrftoken = getCookie('csrftoken');


document.getElementById('like-for-post').addEventListener('click', e => {
    e.preventDefault();
    const url = '{% url "tweets:like" tweet.pk %}';
    fetch(url, {
        method: 'POST',
        body: `tweet_pk={{tweet.pk}}`,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'X-CSRFToken': csrftoken,
        },
    }).then(response => {
        return response.json();
    }).then(response => {
        // イイね数を書き換える
        const counter = document.getElementById('like-for-tweet-count')
        counter.textContent = response.like_for_post_count
        const icon = document.getElementById('like-for-tweet-icon')
        // 作成した場合はハートを塗る
        if (response.method == 'create') {
            icon.classList.remove('far')
            icon.classList.add('fas')
            icon.id = 'like-for-tweet-icon'
        } else {
            icon.classList.remove('fas')
            icon.classList.add('far')
            icon.id = 'like-for-tweet-icon'
        }
    }).catch(error => {
        console.log(error);
    });
});
