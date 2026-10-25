document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('player-form');
    const tableBody = document.getElementById('player-table-body');

    // Função para carregar os jogadores do servidor
    async function loadPlayers() {
        try {
            const response = await fetch('/api/players');
            const players = await response.json();

            tableBody.innerHTML = '';

            players.forEach((player, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td><strong>${player.username}</strong></td>
                    <td>${player.score}</td>
                    <td>${player.headshots}</td>
                `;
                tableBody.appendChild(row);
            });
        } catch (error) {
            console.error('Erro ao carregar jogadores:', error);
        }
    }

    // Função para adicionar um novo jogador via requisição POST
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const username = document.getElementById('username').value;
        const score = parseInt(document.getElementById('score').value);
        const headshots = parseInt(document.getElementById('headshots').value);

        try {
            const response = await fetch('/api/players', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, score, headshots })
            });

            if (response.ok) {
                form.reset();
                loadPlayers();
            } else {
                const data = await response.json();
                alert(data.error || 'Erro ao cadastrar jogador');
            }
        } catch (error) {
            console.error('Erro ao salvar jogador:', error);
        }
    });

    // Carrega a lista ao iniciar
    loadPlayers();
});

