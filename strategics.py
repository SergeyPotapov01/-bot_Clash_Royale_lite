import time
from random import randint, choice

from Bot import Bot
from ImageTriggers import ImageTriggers

from loguru import logger


class Strategics:
    def __init__(self, batlle_mode, open_chest, requested_card, port, changed_account, number_account, total_accounts, id_card, play_clan_war, connection_to_parent):
        self.bot = Bot(port=port)
        self.triggers = ImageTriggers(open_chest, requested_card)
        self.index = 0
        self.index124 = 0
        self.index280 = 0
        self.cycleStart = True
        self.batlle_mode = batlle_mode
        self.number_account = number_account
        self.changed_account = changed_account
        self.total_accounts = total_accounts
        self.connection_to_parent = connection_to_parent
        self.request_card = requested_card
        self.id_card = id_card
        self.play_clan_war = play_clan_war
        self.CW = play_clan_war

    def main(self):
        if self.bot.ADB.cheakInstallCR() == False:
            self.cycleStart = False

        if self.bot.ADB.cheakRunCR() == False:
            self.bot.openCR()

        slowdown_in_menu = True

        index_batlle = 0
        t = time.time()
        while self.cycleStart:
            image = self.bot.getScreen()
            triggers = self.triggers.getTrigger(image)
            trigger = triggers[0]
            logger.debug(str(triggers) + ' ' + str(time.time() - t))
            self.connection_to_parent._textBrowser_3 = f'{triggers}\n' + self.connection_to_parent._textBrowser_3

            if self.index == 50:
                self.bot.reboot()
                self.index = 0
                continue

            if self.index % 5 == 4:
                self.bot.returnHome()
                self.bot.choose_reward(randint(0, 1))

            if self.index124 >= 25:
                self.bot.goToShop()
                self.bot.returnHome()
                self.bot.reboot()
                self.index124 = 0
                continue

            if trigger == 124:
                self.index124 += 1
                continue
            self.index124 = 0

            if not (trigger == 0):
                self.index = 0

            if trigger == 500:
                self.bot.openCR()

            if trigger == 501:
                self.connection_to_parent._textBrowser_3 = 'INCORRECT SCREEN RESOLUTION IS SET!'
                self.stopFarm()

            if trigger == 0:
                self.index += 1
                logger.debug('Не найден триггер')
                time.sleep(3)
                continue
            else:
                self.index = 0

            if trigger == 100:
                if triggers[1] <= 4:
                    continue

                self.bot.selectCard(randint(0, 3))
                self.bot.placingCard1X1(randint(275, 475), randint(426, 700))

            elif trigger == 121:
                index_batlle += 1
                self.bot.exitBatle1X1()
                self.connection_to_parent.totall_batlles += 1
                self.connection_to_parent.got_crowns += triggers[1]
                self.connection_to_parent._textBrowser_2 = f'{triggers[1]}\n' + self.connection_to_parent._textBrowser_2
                self.connection_to_parent._textBrowser_3 = f'{triggers}\n'

                if index_batlle == 10:
                    self.bot.reboot()
                    index_batlle = 0
                time.sleep(3)

            elif trigger == 122:
                self.bot.exitBatle2X2()
                index_batlle += 1
                self.connection_to_parent.totall_batlles += 1
                self.connection_to_parent.got_crowns += triggers[1]
                self.connection_to_parent._textBrowser_2 = f'{triggers[1]}' + self.connection_to_parent._textBrowser_2
                self.connection_to_parent._textBrowser_3 = f'{triggers}\n'
                if index_batlle == 10:
                    self.bot.reboot()
                    index_batlle = 0
                time.sleep(3)

            elif trigger == 124:
                self.bot.ADB.click(400, 420)
                time.sleep(1)

            elif trigger == 200:

                if self.CW:
                    self.bot.goToClanChat()
                    time.sleep(5)
                    image = self.bot.getScreen()
                    triggers = self.triggers.getTrigger(image)
                    trigger = triggers[0]
                    if trigger == 211 and True in triggers[1]:
                        while True:
                            self.bot.swipe_clan_war()
                            time.sleep(2)
                            image = self.bot.getScreen()
                            triggers = self.triggers.getTrigger(image)
                            trigger = triggers[0]
                            if trigger == 260:
                                self.bot.go_batlle_clan_war()
                                break
                        continue
                    elif trigger == 212:
                        self.bot.goToClanChat()
                        time.sleep(1)
                        self.bot.returnHome()
                        continue

                    if trigger == 211 and not (True in triggers[1]):
                        self.CW = False

                if slowdown_in_menu:
                    slowdown_in_menu = False
                    time.sleep(3)
                    continue
                slowdown_in_menu = True

                if 'Until Chest Slots Full':
                    if self.batlle_mode == 'global':
                        self.bot.runBattleGlobal()
                    elif self.batlle_mode == 'disabled':
                        if self.changed_account:
                            self.increasing_account_number()
                            self.bot.changeAccount(self.number_account, self.total_accounts)
                            self.connection_to_parent.number_account = self.number_account
                            self.CW = self.play_clan_war
                        else:
                            self.bot.closeCR()
                            time.sleep(60*60)
                            self.bot.openCR()
                    else:
                        self.bot.runBattleMode(self.batlle_mode)
                    time.sleep(1)

            elif trigger == 210:
                self.bot.goToClanChat()
                time.sleep(2)
                image = self.bot.getScreen()
                triggers = self.triggers.getTrigger(image)
                time.sleep(2)
                trigger = triggers[0]
                if trigger != 212:
                    self.bot.goToClanChat()
                    time.sleep(2)
                self.bot.requestCard(self.id_card)
                time.sleep(4)

            elif trigger == 211:
                self.bot.goToClanChat()
                time.sleep(2)
                image = self.bot.getScreen()
                triggers = self.triggers.getTrigger(image)
                trigger = triggers[0]
                time.sleep(2)
                if trigger != 212:
                    self.bot.goToClanChat()
                    time.sleep(2)
                self.bot.returnHome()

            elif trigger == 212:
                self.bot.returnHome()

            elif trigger == 219:
                self.id_card += 1
                self.bot.reboot()

            elif trigger > 220 and trigger < 225:
                self.bot.getRewardChest(trigger - 220)

            elif trigger == 225:
                self.bot.returnHome()
                time.sleep(0.5)

            elif trigger == 226:
                self.bot.choose_reward(randint(0, 1))
                time.sleep(0.5)

            elif trigger > 230 and trigger < 235:
                self.bot.openChest(trigger - 230)

            elif trigger == 235:
                self.bot.open_pass_royale()

            elif trigger == 236:
                self.bot.goToShop()
                x = 0
                while True:
                    x += 1
                    self.bot.swipe_shop()
                    image = self.bot.getScreen()
                    triggers = self.triggers.getTrigger(image)
                    trigger = triggers[0]
                    if trigger == 237 and x >=4:
                        break
                self.bot.get_shop_reward()
                self.bot.returnHome()
                continue

            elif trigger == 250:
                if self.changed_account:
                    self.increasing_account_number()

                    if self.batlle_mode == 'global':
                        self.bot.skipLimit()
                    else:
                        self.bot.returnHome()

                    triggers = self.triggers.getTrigger(image)
                    trigger = triggers[0]

                    if trigger == 200:
                        self.bot.changeAccount(self.number_account, self.total_accounts)
                        self.connection_to_parent.number_account = self.number_account
                    else:
                        self.bot.returnHome()
                        self.bot.changeAccount(self.number_account, self.total_accounts)
                        self.connection_to_parent.number_account = self.number_account
                    continue
                else:
                    self.bot.rewardLimit()

            elif trigger == 260:
                pass

            elif trigger == 261:
                pass

            elif trigger == 270:
                self.index += 1
                if self.index >= 5:
                    self.bot.setEnglishLanguage()
                else:
                    self.bot.returnHome()
                    time.sleep(2)
                    continue

            elif trigger == 280:
                self.index280 += 1
                if self.index280 >= 10:
                    self.bot.reboot()
                    self.index280 = 0
                self.bot.ADB.click(triggers[1], triggers[2])

            elif trigger == 281:
                self.bot.ADB.click(triggers[1], triggers[2])

            elif trigger == 400:
                time.sleep(120)
                self.bot.exitBatle1X1()

            t = time.time()

    def increasing_account_number(self):
        self.number_account += 1
        if self.number_account >= self.total_accounts:
            self.number_account = 0

    def startFarm(self):
        self.cycleStart = True
        self.main()

    def stopFarm(self):
        self.cycleStart = False