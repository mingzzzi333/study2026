document.addEventListener('DOMContentLoaded', () => {
    // 1. Form submit animation & validation
    const postForm = document.getElementById('postForm');
    const titleInput = document.getElementById('title');
    const messageInput = document.getElementById('message');
    const submitBtn = postForm.querySelector('.btn-submit');

    postForm.addEventListener('submit', (e) => {
        const title = titleInput.value.trim();
        const message = messageInput.value.trim();

        if (!title || !message) {
            e.preventDefault();
            alert('제목과 메시지를 모두 입력해주세요.');
            return;
        }

        // Add loading state to button
        submitBtn.disabled = true;
        const btnText = submitBtn.querySelector('span');
        const btnIcon = submitBtn.querySelector('i');
        
        btnText.textContent = '기록하는 중...';
        btnIcon.className = 'fa-solid fa-circle-notch fa-spin';
    });

    // 2. Relative time formatting
    const timeElements = document.querySelectorAll('.card-date');
    
    function parseUTC(dateString) {
        // SQLite's CURRENT_TIMESTAMP returns YYYY-MM-DD HH:MM:SS in UTC.
        // We need to parse it correctly in a cross-browser compatible way.
        // Split components: "2026-05-21 02:40:00" -> ["2026", "05", "21", "02", "40", "00"]
        const parts = dateString.split(/[- :]/);
        if (parts.length >= 6) {
            // Month is 0-indexed in JS Date constructor (0-11)
            return new Date(Date.UTC(parts[0], parts[1] - 1, parts[2], parts[3], parts[4], parts[5]));
        }
        return new Date(dateString); // fallback
    }

    function getRelativeTime(date) {
        const now = new Date();
        const diffMs = now - date;
        const diffSec = Math.floor(diffMs / 1000);
        const diffMin = Math.floor(diffSec / 60);
        const diffHr = Math.floor(diffMin / 60);
        const diffDay = Math.floor(diffHr / 24);

        if (diffSec < 60) {
            return '방금 전';
        } else if (diffMin < 60) {
            return `${diffMin}분 전`;
        } else if (diffHr < 24) {
            return `${diffHr}시간 전`;
        } else if (diffDay < 7) {
            return `${diffDay}일 전`;
        } else {
            // Format to YYYY.MM.DD
            const yyyy = date.getFullYear();
            const mm = String(date.getMonth() + 1).padStart(2, '0');
            const dd = String(date.getDate()).padStart(2, '0');
            return `${yyyy}.${mm}.${dd}`;
        }
    }

    function updateTimes() {
        timeElements.forEach(el => {
            const rawTime = el.getAttribute('data-time');
            if (rawTime) {
                const utcDate = parseUTC(rawTime);
                el.innerHTML = `<i class="fa-regular fa-clock"></i> ${getRelativeTime(utcDate)}`;
                // Set original timestamp as tooltip
                el.title = utcDate.toLocaleString();
            }
        });
    }

    updateTimes();
    // Update every minute
    setInterval(updateTimes, 60000);

    // 3. Staggered card animation (if cards grid exists)
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.05}s`;
    });
});
