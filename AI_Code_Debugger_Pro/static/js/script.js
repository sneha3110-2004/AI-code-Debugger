console.log("Script.js has loaded!"); // This will show in F12 Console

document.addEventListener('DOMContentLoaded', () => {
    const themeBtn = document.getElementById('theme-toggle');
    const analyzeBtn = document.getElementById('btn');

    // 1. Theme Toggle Logic
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', newTheme);
            console.log("Theme switched to: " + newTheme);
        });
    }

    // 2. Analyze Button Logic
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', async () => {
            console.log("Analyze button clicked!");
            const code = document.getElementById('code').value;
            const output = document.getElementById('output');
            
            if(!code) {
                alert("Please paste code!");
                return;
            }

            output.innerText = "Processing...";
            
            try {
                const response = await fetch('/debug', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ code: code, language: 'python' })
                });
                const data = await response.json();
                output.innerText = data.analysis || data.error;
            } catch (err) {
                output.innerText = "Server Error. Is Python running?";
            }
        });
    }
});