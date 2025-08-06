// Simplified modal system - no freeze guaranteed
class SimpleModalSystem {
    openDevotion() {
        // Remove any existing modals first
        document.querySelectorAll('.simple-modal').forEach(el => el.remove());
        
        const modalHTML = `
        <div class="simple-modal" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 9999; display: flex; align-items: center; justify-content: center;">
            <div style="background: white; border-radius: 8px; max-width: 600px; width: 90%; max-height: 80%; overflow-y: auto; position: relative;">
                <div style="padding: 20px; border-bottom: 1px solid #ddd; background: #007bff; color: white; display: flex; justify-content: space-between; align-items: center;">
                    <h5 style="margin: 0;">Daily Devotion</h5>
                    <button onclick="this.closest('.simple-modal').remove()" style="background: none; border: none; color: white; font-size: 24px; cursor: pointer;">&times;</button>
                </div>
                <div style="padding: 20px;" id="simple-content">
                    <div style="text-align: center;">Loading...</div>
                </div>
            </div>
        </div>`;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Load content
        fetch('/api/gamified/daily_devotion')
            .then(response => response.json())
            .then(data => {
                if (data.type === 'already_completed') {
                    document.getElementById('simple-content').innerHTML = `
                        <div style="text-align: center;">
                            <h5>Devotion Complete!</h5>
                            <p>${data.message}</p>
                            <p>Current streak: ${data.streak} days</p>
                            <button onclick="this.closest('.simple-modal').remove()" style="padding: 10px 20px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">Close</button>
                        </div>
                    `;
                } else {
                    const devotion = data.devotion;
                    document.getElementById('simple-content').innerHTML = `
                        <h6 style="color: #007bff;">${devotion.passage}</h6>
                        <blockquote style="border-left: 4px solid #007bff; padding-left: 15px; margin: 15px 0;">
                            "${devotion.text}"
                        </blockquote>
                        <p>${devotion.insight}</p>
                        <p><strong>Reflection:</strong> ${devotion.reflection}</p>
                        <textarea id="reflection-input" placeholder="Share your thoughts..." style="width: 100%; height: 80px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; margin: 10px 0;"></textarea>
                        <div style="text-align: center; margin-top: 20px;">
                            <button onclick="window.completeSimpleDevotion()" style="padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; margin-right: 10px;">Complete (+2 XP)</button>
                            <button onclick="this.closest('.simple-modal').remove()" style="padding: 10px 20px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">Cancel</button>
                        </div>
                    `;
                }
            })
            .catch(error => {
                document.getElementById('simple-content').innerHTML = `
                    <div style="text-align: center; color: red;">
                        Failed to load devotion. Please try again.
                        <br><br>
                        <button onclick="this.closest('.simple-modal').remove()" style="padding: 10px 20px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">Close</button>
                    </div>
                `;
            });
    }
    
    completeDevotion() {
        const reflection = document.getElementById('reflection-input')?.value || '';
        
        fetch('/api/gamified/complete_devotion', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reflection })
        })
        .then(response => response.json())
        .then(result => {
            alert(`Devotion completed! +${result.xp_earned || 2} XP earned!`);
            document.querySelector('.simple-modal')?.remove();
        })
        .catch(error => {
            alert('Failed to complete devotion. Please try again.');
        });
    }
}

// Create global instance
window.simpleModal = new SimpleModalSystem();
window.completeSimpleDevotion = () => window.simpleModal.completeDevotion();