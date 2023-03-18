local function assignBag(index,player)

    if player:getHoursSurvived() == 0.000 then

        player:getInventory():AddItem("TwitchSurvivors.Bag_TwitchSurvivors")

    end
end

Events.OnCreatePlayer.Add(assignBag)
