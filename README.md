# **Mario Jumper - Game Design Document**

The repository contains a prototype implementation of a game in Pygame, which was implemented as a final project for the Object Technologies course.

**Author**: Filip Prešnajder

**Chosen theme**: Dark and Light

---
## **1. Introduction**
The proposed game serves as a presentation for the final project for the subject Object Technologies. The created game meets the requirements of the assigned topic (Dark and Light). The game has a player (Mario) set in two levels, the first is the day/light level and the second is night/dark level, his goal is to pass all the enemies and obstacles to win.

### **1.1 Inspiration**
<ins>**Super Mario**</ins>

Super Mario is a platform game series created by Nintendo starring their mascot, Mario. The objective of the game is to progress through levels by defeating enemies, collecting items and solving puzzles without dying.

<p align="center">
  <img src="https://ew.com/thmb/MXdm_2NC883VoKwPNdwYh24aa1k=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/super-mario-bros-7f3c67482caa4f34b39cda5c19efd63d.jpg" alt="Super Mario">
  <br>
  <em>Figure 1 Preview of Super Mario</em>
</p>

### **1.2 Player Experience**
The goal of the game is for the player to pass all the levels without dying by either falling or hitting an enemy. He can either or move to the left or to the right. The player can also shoot bullets opposed to the fireballs in an original Mario to hit enemies.

### **1.3 Development Software**
- **Pygame-CE**: chosen programming language.
- **IntelliJ IDEA 2024.1**: chosen IDE.
- **Itch.io**: [here](https://itch.io/)

---
## **2. Concept**

### **2.1 Gameplay Overview**
The player controls his character and during the gameplay tries to pass the level without dying. He is able to jump up and hit bonus blocks with his head to pick up either a coin or a bullet. He can then either stomp or shoot at the enemies to destroy them. By picking coins, hitting bonus blocks or destryoing enemies he gains 100 score for each. To prevent player from spamming his shooting, each shot has a 0.5 seconds cooldown.

### **2.2 Theme Interpretation**
**"Dark and Light"** - The first level is the light level which is set in a day time where as the second level is a dark theme which is set in a night time. For the night time almost all the sprites and textures change to fit in the theme and also the whole soundtrack changes, having a more "night" vibe.

### **2.3 Primary Mechanics**
- **Platforms**: The player can jump up on these platforms to progress through a map
- **Sprinting**: The player can hold the spacebar to sprint to increase its speed.
- **Bonuses**: The player can pick up bonuses which either coins or bullets for extra score and with bullets to shoot the enemies. 
- **Set enemy movement**: If the enemy is deemed far away from the player he will not be initially moving (for example at the start, player is at the very left and the enemy is at the right of the map), this is because they would never meet and enemy would fall off the map in most cases. So the enemy only starts moving once the player is close enough.
- **The player can eliminate enemies**: the player shoots a bullet that, when hitting an enemy, eliminates it, or he can jump and land on the enemy, effectivelly "stomping" on them to eliminate them.

### **2.4 Class design**
- **Game**: class that contains the main important aspects of the game and communicates with the main function to render all the assets and perform all the actions.
- **Player**: class representing the player, player control, character rendering and abilities.
- **Enemy**: class of enemies, their game logic and movement.
- **Bullet**: class of a bullet, it's movement logic and hit logic.
- **Bonus**: class of a bonus block, it's rendering, actions to take once hit.
- **Brick & Block**: classes of standard building blocks.
- **Pipe**: class for the pipe which is at the end of the map that the player can interact with once he stands on top of it.

---
## **3. Art**

### **3.1 Theme Interpretation**
The game wants to be visually appealing, where using assets from [itch.io](https://webfussel.itch.io/more-bit-8-bit-mario), the player's and enemies assets were selected,as for the enemies and blocks, their visual appearence changes on the level the player is at, the art concpet is an 8-bit art concept in 2D.

<p align="center">
  <img src="https://github.com/filippresnajder/mario_jumper/blob/main/assets/enemies/day/gnom.png" alt="Day gnom sprite">
  <img src="https://github.com/filippresnajder/mario_jumper/blob/main/assets/enemies/day/turtle.png" alt="Day turtle sprite">
  <br>
  <em>Figure 2 Preview of enemy day sprites</em>
</p>

<p align="center">
  <img src="https://github.com/filippresnajder/mario_jumper/blob/main/assets/enemies/night/gnom.png" alt="Night gnom sprite">
  <img src="https://github.com/filippresnajder/mario_jumper/blob/main/assets/enemies/night/turtle.png" alt="Night turtle sprite">
  <br>
  <em>Figure 3 Preview of enemy night sprites</em>
</p>

### **3.2 Design**
The game uses assets from itch.io, The goal was to achieve a visually pleasing design with a hint of the classic Super Mario vibe. Additional levels will be based on the same assets, combining different blocks and enemies.

<p align="center">
  <img src="https://github.com/filippresnajder/mario_jumper/blob/main/level.png" alt="Level design">
  <br>
  <em>Figure 4 Level design concept</em>
</p>

---
## **4. Audio**

### **4.1 Music**
The selection of background music was focused on a Super Mario like music, more specifically from Mario Forever [here](https://www.youtube.com/watch?v=_3MWOsMKsts&list=PLni4--hlvTwjomUVn6DsgrvT3rKwgIjRt&index=37&ab_channel=Safarifire) Level 1-3 for level 1 and Mario Forever Level 3-3 for level 2 [here](https://www.youtube.com/watch?v=GSW2jtiS0dE&list=PLni4--hlvTwjomUVn6DsgrvT3rKwgIjRt&index=5&ab_channel=Safarifire).

### **4.2 Sound Efects**
The sounds in the game were similarly oriented towards Super mario sounds, reusing assets from [here](https://themushroomkingdom.net/media/smb/wav), from which the sound for the coins, bullet, jumping, stomping, game win and game over were selected.

---
## **5. Game Experience**

### **5.1 UI**
The user interface is pretty simple just like in normal Super Mario except on the top left, the player can see his score and on the right he can see his amount of ammuniton he has left.

### **5.2 Controls**
<ins>**Keyboard**</ins>
- **WAD**: Move the player around the map.
- **SPACE**: Sprint
- **S**: Interracting with pipe to finish the game or get to another level
- **Q**: Shoot.
- **ESC**: Exit game.
- **R**: Restart game.
