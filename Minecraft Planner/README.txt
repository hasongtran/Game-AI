P5: GOAP in Minecraft Planning
Partners: Ha Song Tran, Jasper Yeh

Approach/Algorithm:
We began with implementing our A* approach for the craft planning. Our A* included a basic approach similar to P2 with a few adjustments. We then began testing the test cases and was successful until crafting iron_pickaxe. We had some trouble implementing our heuristics. Our goal was to limit the "crafting tools" to one each and have the program return infinity and skip over the instances where it would look over the crafting step in the recipe. We also tried to limit the crafting of the axe tools to one each due to the fact that you'd only need one axe tool for each instance of the recipe.

We ran into trouble implementing this heuristic, however and was unable to run it. So the current code we have is one with the written heuristic commented out and A* completely working. Our approach was not able to craft any item that included ingots in the recipe under thirty seconds. Also, crafting multiple of the same objects often resulted in abnormally large  search times. For example, crafting a single furnace would take about two seconds, but crafting two furnaces would take about 200 seconds.

The hardest problem our algorithm can solve is to have the goal be:
    Goal: {'bench': 1, 'plank': 1, 'wooden_pickaxe': 1, 'stone_pickaxe': 1, 'cobble': 1, 'ore': 1, 'furnace': 1}
Our algorithm was able to solve this in 14.33383860901813 seconds, running on the slower computer.

