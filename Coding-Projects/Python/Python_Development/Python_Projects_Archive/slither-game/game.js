class Vector {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

class Food {
    constructor(game) {
        this.game = game;
        this.x = Math.random() * game.worldSize;
        this.y = Math.random() * game.worldSize;
        this.radius = 5 + Math.random() * 5;
        this.color = `hsl(${Math.random() * 360}, 100%, 50%)`;
        this.value = this.radius; // Score value
    }

    draw(ctx) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.color;
        ctx.closePath();
        ctx.shadowBlur = 0;
    }
}

class Snake {
    constructor(game, x, y, isBot = false) {
        this.game = game;
        this.x = x;
        this.y = y;
        this.isBot = isBot;
        this.angle = Math.random() * Math.PI * 2;
        this.baseSpeed = 3;
        this.speed = this.baseSpeed;
        this.turnSpeed = 0.08;
        this.radius = 10;
        this.segments = [];
        this.length = 10; // Initial length
        this.color = isBot ? `hsl(${Math.random() * 360}, 70%, 50%)` : '#00ff00';
        this.score = 0;

        // Abilities
        this.magnetRange = 0; // Base pickup range bonus
        this.canGrab = false;
        this.isGrabbing = false;

        if (!isBot) {
            // Apply upgrades
            if (game.upgrades.magnet) this.magnetRange = 50; // Vacuum radius
            if (game.upgrades.grab) this.canGrab = true;
            if (game.upgrades.speed) this.baseSpeed = 4.5; // 50% faster
        }
        this.speed = this.baseSpeed;

        // Initialize segments
        for (let i = 0; i < this.length; i++) {
            this.segments.push({ x: this.x, y: this.y });
        }
    }

    update() {
        // Target angle
        let targetAngle;
        if (this.isBot) {
            // Simple Bot AI: Move randomly or towards food
            if (Math.random() < 0.02) {
                this.targetAngle = Math.random() * Math.PI * 2;
            }

            // Avoid player if grabbing
            if (this.game.player && this.game.player.isGrabbing) {
                const dx = this.game.player.x - this.x;
                const dy = this.game.player.y - this.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 400) { // Increased grab range
                    // Being pulled!
                    // STUN LOGIC: Force angle towards player
                    this.targetAngle = Math.atan2(dy, dx);
                    this.speed = 8; // Pulled very fast
                } else {
                    this.speed = 3; // Reset speed if out of range
                }
            } else {
                this.speed = 3; // Normal bot speed
            }

            if (!this.targetAngle) this.targetAngle = this.angle;
            targetAngle = this.targetAngle;
        } else {
            // Player follows mouse
            const mouseWorldX = this.game.mouseX + this.game.camera.x;
            const mouseWorldY = this.game.mouseY + this.game.camera.y;
            targetAngle = Math.atan2(mouseWorldY - this.y, mouseWorldX - this.x);

            // Handle Grab Ability
            if (this.canGrab && this.game.keys[' ']) {
                this.isGrabbing = true;
            } else {
                this.isGrabbing = false;
            }
        }

        // Smooth turning
        let diff = targetAngle - this.angle;
        while (diff < -Math.PI) diff += Math.PI * 2;
        while (diff > Math.PI) diff -= Math.PI * 2;

        if (Math.abs(diff) < this.turnSpeed) {
            this.angle = targetAngle;
        } else {
            this.angle += Math.sign(diff) * this.turnSpeed;
        }

        // Move head
        this.x += Math.cos(this.angle) * this.speed;
        this.y += Math.sin(this.angle) * this.speed;

        // Boundary check
        this.x = Math.max(0, Math.min(this.game.worldSize, this.x));
        this.y = Math.max(0, Math.min(this.game.worldSize, this.y));

        // Update segments
        // Add new head position
        this.segments.unshift({ x: this.x, y: this.y });

        // Remove tail segments to match length
        // We keep segments based on distance to create the slither effect
        // Actually, a simpler way for "Slither" style is to store history and sample at intervals
        // But for simplicity, we'll just limit the array size based on length * spacing
        const spacing = 5;
        if (this.segments.length > this.length * spacing) {
            this.segments.pop();
        }
    }

    draw(ctx) {
        // Draw Grab Effect
        if (this.isGrabbing) {
            ctx.beginPath();
            ctx.arc(this.x, this.y, 400, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(255, 0, 0, 0.1)'; // Red tint for aggressive grab
            ctx.fill();
            ctx.strokeStyle = 'rgba(255, 0, 0, 0.3)';
            ctx.stroke();
        }

        ctx.fillStyle = this.color;
        const spacing = 5;

        // Draw segments from tail to head
        for (let i = this.segments.length - 1; i >= 0; i -= spacing) {
            const segment = this.segments[i];
            ctx.beginPath();
            ctx.arc(segment.x, segment.y, this.radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.closePath();
        }

        // Draw eyes for head
        ctx.fillStyle = 'white';
        const eyeOffset = this.radius * 0.6;
        const eyeX1 = this.x + Math.cos(this.angle - 0.5) * eyeOffset;
        const eyeY1 = this.y + Math.sin(this.angle - 0.5) * eyeOffset;
        const eyeX2 = this.x + Math.cos(this.angle + 0.5) * eyeOffset;
        const eyeY2 = this.y + Math.sin(this.angle + 0.5) * eyeOffset;

        ctx.beginPath();
        ctx.arc(eyeX1, eyeY1, this.radius * 0.4, 0, Math.PI * 2);
        ctx.arc(eyeX2, eyeY2, this.radius * 0.4, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = 'black';
        ctx.beginPath();
        ctx.arc(eyeX1 + Math.cos(this.angle) * 2, eyeY1 + Math.sin(this.angle) * 2, this.radius * 0.2, 0, Math.PI * 2);
        ctx.arc(eyeX2 + Math.cos(this.angle) * 2, eyeY2 + Math.sin(this.angle) * 2, this.radius * 0.2, 0, Math.PI * 2);
        ctx.fill();
    }

    grow(amount) {
        this.length += amount;
        this.score += amount;
        this.radius = Math.min(25, 10 + this.length * 0.05);
    }
}

class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.width = window.innerWidth;
        this.height = window.innerHeight;

        this.score = 0;
        this.gems = 0;
        this.scoreSinceLastGem = 0;
        this.isRunning = false;

        // Upgrades
        this.upgrades = {
            magnet: false,
            grab: false,
            speed: false,
            double_gems: false
        };

        // Inputs
        this.mouseX = this.width / 2;
        this.mouseY = this.height / 2;
        this.keys = {};

        // Game World
        this.worldSize = 3000;
        this.camera = { x: 0, y: 0 };

        this.player = null;
        this.foods = [];
        this.bots = [];

        this.init();
        this.setupEventListeners();
        this.updateStoreUI();
    }

    init() {
        this.resize();
    }

    resize() {
        this.width = window.innerWidth;
        this.height = window.innerHeight;
        this.canvas.width = this.width;
        this.canvas.height = this.height;
    }

    setupEventListeners() {
        window.addEventListener('resize', () => this.resize());
        window.addEventListener('mousemove', (e) => {
            this.mouseX = e.clientX;
            this.mouseY = e.clientY;
        });
        window.addEventListener('keydown', (e) => this.keys[e.key] = true);
        window.addEventListener('keyup', (e) => this.keys[e.key] = false);

        document.getElementById('start-btn').addEventListener('click', () => this.startGame());
        document.getElementById('restart-btn').addEventListener('click', () => this.startGame());

        // Store Buttons
        const openStore = () => {
            document.getElementById('start-screen').classList.add('hidden');
            document.getElementById('game-over-screen').classList.add('hidden');
            document.getElementById('store-screen').classList.remove('hidden');
            this.updateStoreUI();
        };

        document.getElementById('shop-btn-main').addEventListener('click', openStore);
        document.getElementById('shop-btn-start').addEventListener('click', openStore);
        document.getElementById('shop-btn-over').addEventListener('click', openStore);

        document.getElementById('close-store-btn').addEventListener('click', () => {
            document.getElementById('store-screen').classList.add('hidden');
            document.getElementById('start-screen').classList.remove('hidden');
        });

        // Buy Buttons
        document.querySelectorAll('.buy-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const item = e.target.dataset.item;
                const price = parseInt(e.target.dataset.price);
                this.buyItem(item, price);
            });
        });
    }

    buyItem(item, price) {
        if (this.gems >= price) {
            if (item === 'growth') {
                // Consumable
                this.gems -= price;
                if (this.player) this.player.grow(20);
                this.updateStoreUI();
                return;
            }

            if (!this.upgrades[item]) {
                this.gems -= price;
                this.upgrades[item] = true;

                // Apply immediate effects
                if (item === 'speed' && this.player) {
                    this.player.baseSpeed = 4.5;
                    this.player.speed = 4.5;
                }

                this.updateStoreUI();
                this.updateHUD();
            }
        }
    }

    updateStoreUI() {
        document.getElementById('store-gem-count').innerText = this.gems;
        document.getElementById('gems').innerText = this.gems;

        // Update buttons
        const items = ['magnet', 'grab', 'speed', 'double_gems'];
        items.forEach(item => {
            const btn = document.querySelector(`.buy-btn[data-item="${item}"]`);
            if (this.upgrades[item]) {
                btn.innerText = "Owned";
                btn.disabled = true;
                document.getElementById(`item-${item}`).classList.add('owned');
            }
        });
    }

    updateHUD() {
        if (this.upgrades.magnet) document.getElementById('slot-magnet').classList.add('unlocked');
        if (this.upgrades.grab) document.getElementById('slot-grab').classList.add('unlocked');
    }

    startGame() {
        this.score = 0;
        this.scoreSinceLastGem = 0;
        this.isRunning = true;
        document.getElementById('start-screen').classList.add('hidden');
        document.getElementById('game-over-screen').classList.add('hidden');
        document.getElementById('store-screen').classList.add('hidden');
        document.getElementById('score').innerText = Math.floor(this.score);

        this.updateHUD();

        // Reset entities
        this.player = new Snake(this, this.worldSize / 2, this.worldSize / 2);
        this.foods = [];
        this.bots = [];

        // Spawn initial food
        for (let i = 0; i < 500; i++) {
            this.foods.push(new Food(this));
        }

        // Spawn bots
        for (let i = 0; i < 20; i++) {
            this.bots.push(new Snake(this, Math.random() * this.worldSize, Math.random() * this.worldSize, true));
        }

        this.loop();
    }

    gameOver() {
        this.isRunning = false;
        document.getElementById('final-score').innerText = Math.floor(this.score);
        document.getElementById('final-gems').innerText = this.gems; // Show total gems
        document.getElementById('game-over-screen').classList.remove('hidden');
    }

    update() {
        if (!this.isRunning) return;

        this.player.update();

        // Update Bots
        this.bots.forEach(bot => bot.update());

        // Camera follow player
        this.camera.x = this.player.x - this.width / 2;
        this.camera.y = this.player.y - this.height / 2;

        // Clamp camera to world bounds
        this.camera.x = Math.max(0, Math.min(this.worldSize - this.width, this.camera.x));
        this.camera.y = Math.max(0, Math.min(this.worldSize - this.height, this.camera.y));

        // Collision Detection

        // 1. Player vs Food
        for (let i = this.foods.length - 1; i >= 0; i--) {
            const food = this.foods[i];
            const dx = this.player.x - food.x;
            const dy = this.player.y - food.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            // Magnet Ability check
            const pickupRadius = this.player.radius + food.radius + this.player.magnetRange;

            if (dist < pickupRadius) {
                // If using magnet, pull food in first (visual effect)
                if (dist > this.player.radius + food.radius) {
                    food.x += (this.player.x - food.x) * 0.1;
                    food.y += (this.player.y - food.y) * 0.1;
                    continue; // Don't eat yet, just pull
                }

                this.player.grow(food.value / 10);
                this.score += food.value;

                // Gem Logic: 5 points = 1 Gem
                this.scoreSinceLastGem += food.value;
                if (this.scoreSinceLastGem >= 5) {
                    let gemsEarned = Math.floor(this.scoreSinceLastGem / 5);
                    if (this.upgrades.double_gems) gemsEarned *= 2; // Double Gems
                    this.gems += gemsEarned;
                    this.scoreSinceLastGem %= 5;
                    document.getElementById('gems').innerText = this.gems;
                    this.updateStoreUI();
                }

                document.getElementById('score').innerText = Math.floor(this.score);
                this.foods.splice(i, 1);
                this.foods.push(new Food(this)); // Respawn food
            }
        }

        // 2. Player vs Bots (Collision with body)
        // Check if player head hits any bot body
        for (const bot of this.bots) {
            // Check player hitting bot
            if (this.checkCollision(this.player, bot)) {
                this.gameOver();
                return;
            }

            // Check bot hitting player (kill bot)
            if (this.checkCollision(bot, this.player)) {
                this.killSnake(bot);
            }

            // Bot vs Bot (optional, but good for realism)
            for (const otherBot of this.bots) {
                if (bot !== otherBot && this.checkCollision(bot, otherBot)) {
                    this.killSnake(bot);
                    break;
                }
            }
        }

        // 3. Player vs World Boundaries
        if (this.player.x <= 0 || this.player.x >= this.worldSize ||
            this.player.y <= 0 || this.player.y >= this.worldSize) {
            this.gameOver();
        }
    }

    checkCollision(headSnake, bodySnake) {
        // Head of headSnake vs Body of bodySnake
        const headX = headSnake.x;
        const headY = headSnake.y;
        const headR = headSnake.radius;

        // Optimization: Check bounding box first

        const spacing = 5;
        // Iterate through body segments (skip head segments to avoid self-collision if we want that)
        // For Slither, usually you can cross your own body. So we only check other snakes.

        let startIndex = 0;
        if (headSnake === bodySnake) {
            return false; // Can cross own body in Slither
        }

        for (let i = startIndex; i < bodySnake.segments.length; i += spacing) {
            const seg = bodySnake.segments[i];
            const dx = headX - seg.x;
            const dy = headY - seg.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < headR + bodySnake.radius) {
                return true;
            }
        }
        return false;
    }

    killSnake(snake) {
        // Turn snake body into food
        const spacing = 5;
        for (let i = 0; i < snake.segments.length; i += spacing) {
            const seg = snake.segments[i];
            const food = new Food(this);
            food.x = seg.x + (Math.random() - 0.5) * 20;
            food.y = seg.y + (Math.random() - 0.5) * 20;
            food.value = 5; // Dead snake food is valuable
            food.radius = 8;
            this.foods.push(food);
        }

        // Remove snake from bots list
        const index = this.bots.indexOf(snake);
        if (index > -1) {
            this.bots.splice(index, 1);
            // Respawn a new bot
            this.bots.push(new Snake(this, Math.random() * this.worldSize, Math.random() * this.worldSize, true));
        }
    }

    draw() {
        // Clear screen
        this.ctx.fillStyle = '#222';
        this.ctx.fillRect(0, 0, this.width, this.height);

        this.ctx.save();
        // Apply camera transform
        this.ctx.translate(-this.camera.x, -this.camera.y);

        // Draw Grid/Background
        this.drawGrid();

        // Draw Food
        this.foods.forEach(food => {
            // Optimization: Only draw if in view
            if (food.x > this.camera.x - 50 && food.x < this.camera.x + this.width + 50 &&
                food.y > this.camera.y - 50 && food.y < this.camera.y + this.height + 50) {
                food.draw(this.ctx);
            }
        });

        // Draw Bots
        this.bots.forEach(bot => bot.draw(this.ctx));

        // Draw Player
        if (this.player) this.player.draw(this.ctx);

        this.ctx.restore();

        // Draw Mini-map (Optional, maybe later)
    }

    drawGrid() {
        this.ctx.strokeStyle = '#333';
        this.ctx.lineWidth = 1;
        const gridSize = 50;

        // Calculate visible range to optimize rendering
        const startX = Math.floor(this.camera.x / gridSize) * gridSize;
        const endX = startX + this.width + gridSize;
        const startY = Math.floor(this.camera.y / gridSize) * gridSize;
        const endY = startY + this.height + gridSize;

        for (let x = startX; x < endX; x += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, startY);
            this.ctx.lineTo(x, endY);
            this.ctx.stroke();
        }

        for (let y = startY; y < endY; y += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(startX, y);
            this.ctx.lineTo(endX, y);
            this.ctx.stroke();
        }

        // Draw World Borders
        this.ctx.strokeStyle = '#ff0000';
        this.ctx.lineWidth = 5;
        this.ctx.strokeRect(0, 0, this.worldSize, this.worldSize);
    }

    loop() {
        if (!this.isRunning) return;
        this.update();
        this.draw();
        requestAnimationFrame(() => this.loop());
    }
}

// Start the game instance
const game = new Game();
