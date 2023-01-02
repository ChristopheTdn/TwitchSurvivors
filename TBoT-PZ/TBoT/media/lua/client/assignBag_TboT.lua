function assignBag()

    local player = getSpecificPlayer(0)
    TBoTTime = GameTime:getInstance();
    TBoT = TBoTTime:getModData();
    if TBoT.tbag == nil then
        TBoT.tbag=player:getInventory():AddItem("TBoT.Bag_TBoT")
    end
    TBoT.tbag:getInventory():AddItem("Base.Pistol")
end

local function OnInitGlobalModData(isNewGame)
    TBoTable= ModData.getOrCreate(tbagData)
    local player = getSpecificPlayer(0)
    player:Say("initgloabData")
    print("INIT GLOBAL DATA %%%%%%%%%%%%%%%%%%%%%%")
end
Events.OnNewGame.Add(assignBag)
