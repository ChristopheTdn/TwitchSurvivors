function assignBag()
    print(tbag)
    if not tbag then
        print(tbag)
        local player = getSpecificPlayer(0)
        tbag=player:getInventory():AddItem("TBoT.Bag_TBoT")
    end
end
Events.OnNewGame.Add(assignBag)