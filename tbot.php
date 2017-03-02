<?php




class BOT extends TBClient //see https://github.com/wsm3/TelegramBotClient
{
    function __construct()
    {
        parent::__construct('API_TOKEN', 'WEB_HOCK');
        parent::botExecute();
    }

    function bot()
    {

        $this->CreateReplyKeyboard(array(
            'Расписание на сегодня', 'Расписание на завтра', //'Последние результаты'
        ));

        $today = date("d-m-Y");

        switch ($this->getMessage()) {
            case '/start':
            case '/help':
                $mgs = sprintf('Привет, %s! Я бот умеющий показывать расписание футбольных трансляций на ТВ и последние результаты матчей!', $this->getFirstName());
                $this->sendMessage($mgs);
                break;
            case 'расписание на сегодня':
                $file_path = sprintf('./tdata/%s_translations', $today);
                $data = file_get_contents($file_path);

                $this->sendMessage($data);
                break;
            case 'расписание на завтра':
                $file_path = sprintf('./tdata/%s_translations', date('m-d-Y', strtotime($today . "+1 days")));
                $data = file_get_contents($file_path);

                $this->sendMessage($data);
                break;
            case 'последние результаты':
                $file_path = './tdata/last_result';
                $data = file_get_contents($file_path);

                $this->sendMessage($data);
                break;
        }


    }
}


$b = new BOT();
$b->bot();

