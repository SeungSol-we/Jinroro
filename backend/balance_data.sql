--
-- PostgreSQL database dump
--

\restrict hIpmqg5TVp09eMS445ZQFmCcYYuZTu3IQ6KcjApfc3Yrzm8qRp5SlPdycSgEP1Y

-- Dumped from database version 15.18 (Debian 15.18-1.pgdg13+1)
-- Dumped by pg_dump version 15.18 (Debian 15.18-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: fear_tags; Type: TABLE DATA; Schema: public; Owner: careernobox
--

INSERT INTO public.fear_tags VALUES (1, '야근', 1.5, '퇴근 시간 이후에도 일해야 하는 환경');
INSERT INTO public.fear_tags VALUES (2, '반복업무', 1.2, '매일 똑같은 작업이 반복되는 업무');
INSERT INTO public.fear_tags VALUES (3, '강한대인응대', 1.3, '고객/외부인과 잦은 대화가 필요한 업무');
INSERT INTO public.fear_tags VALUES (4, '외근많음', 1, '사무실보다 외부에서 보내는 시간이 많음');
INSERT INTO public.fear_tags VALUES (5, '육체노동', 1.2, '신체를 많이 사용하는 작업');
INSERT INTO public.fear_tags VALUES (6, '혼자일하기', 1, '팀보다 혼자 업무를 처리하는 비중이 높음');
INSERT INTO public.fear_tags VALUES (7, '팀협업', 1, '여러 사람과 긴밀하게 협력해야 하는 환경');
INSERT INTO public.fear_tags VALUES (8, '높은책임감', 1.3, '중요한 결정이나 큰 책임을 지는 역할');
INSERT INTO public.fear_tags VALUES (9, '창의성요구', 1.1, '새로운 아이디어나 창의적 사고가 필요한 업무');
INSERT INTO public.fear_tags VALUES (10, '강한위계질서', 1.2, '상하관계가 뚜렷하고 보고 체계가 복잡한 조직');


--
-- Data for Name: ai_generated_scenarios; Type: TABLE DATA; Schema: public; Owner: careernobox
--

INSERT INTO public.ai_generated_scenarios VALUES (1, 10, 1, '막강한 사무실의 압박', '당신은 상사가 매일 아침 6시 30분에 ''상사님''이라고 부르지 않으면 출근을 못하게 하는 회사에 다니고 있습니다. 그런데 오늘은 상사가 ''상사님'' 대신 ''대통령님''이라고 불러야 한다고 지시했습니다.', '상사가 이틀 후에 ''왕''이라고 부르지 않으면 대기발령을 내리겠다고 협박하는 걸 선택할 수 있습니다.', '상사가 ''오늘 야근은 필수다''라고 외치며 팀원들을 강제로 연장근무 시키는 상황을 선택할 수 있습니다.', '위계질서', '야근', '2026-05-27 03:18:31.245542+00');
INSERT INTO public.ai_generated_scenarios VALUES (2, 4, 1, '출근길의 재앙', '오늘 아침, 당신은 갑자기 우주 공간으로 떨어졌습니다! 지구로 돌아가기 위해 외계인과 계약서를 작성해야 하는데, 그 과정에서 외근을 다녀와야 한다는 조건이 붙었습니다. 하지만 외계인들은 제트팩이 아닌 자전거를 타고 왔다고 합니다!', '자전거를 타고 100km를 외근하며 외계인들에게 무상으로 피자를 배달해야 한다.', '야근을 하며 12시간 동안 외계인과 함께 외계어를 배우는 고통을 겪어야 한다.', '외근많음', '야근', '2026-05-27 03:18:39.012752+00');
INSERT INTO public.ai_generated_scenarios VALUES (3, 2, 8, '무한한 반복의 괴로움', '우주에서 가장 지루한 회의에 참석해, 1시간 동안 매번 똑같은 말만 반복하는 상사를 보며 당신의 눈이 감겨옵니다. 그런데 갑자기, 그 상사가 회의 중 우주 괴물로 변신해버리며 당신에게 책임을 떠넘깁니다!', '상사가 매일 똑같은 내용을 반복하며 당신에게 ''어떻게 생각하냐''고 매번 물어봐서 시간을 갉아먹는 것이 더 싫다.', '괴물이 되어버린 상사가 당신에게 책임을 묻고, ''당신이 모든 걸 해결해야 해!''라고 소리치는 것이 더 싫다.', '반복업무', '높은책임감', '2026-05-27 03:18:45.956819+00');
INSERT INTO public.ai_generated_scenarios VALUES (4, 7, 9, '피자 배달 전쟁', '각자 피자 한 판씩 들고 겨루는 팀 배달 대회! 팀원들이 ''누가 더 빠르게!''라고 외치며 서로의 피자를 발로 차는 상황. 누가 가장 먼저 피자를 배달하나!?', '팀원들이 발로 차인 피자를 다시 조립하면서 협력해야 한다.', '그런데 피자 토핑을 혼자서 무작위로 창의적으로 조합해야 한다.', '협동', '창의성', '2026-05-27 03:18:54.613588+00');
INSERT INTO public.ai_generated_scenarios VALUES (5, 6, 4, '혼자서 마라톤', '당신은 낯선 도시에서 혼자 마라톤을 뛰고 있습니다. 그런데 이곳은 마라톤 중에 외로운 로봇들이 계속 지나가며 당신의 이름을 외치고, 당신은 그들의 인사에 응답해야 합니다.', '혼자 이 로봇들에게 인사하며 마라톤을 계속하는 것.', '지금 당장 로봇과 함께 외근해버리고, 상상도 못한 외부에서 일하는 것.', '고독', '외출', '2026-05-27 03:19:09.26667+00');
INSERT INTO public.ai_generated_scenarios VALUES (6, 2, 10, '사무실의 괴물들', '당신은 매일 아침마다 같은 커피를 타고, 같은 보고서를 작성하는 반복적인 삶을 살고 있다. 그런데 어느 날, 사무실에 신입 직원이 들어왔는데, 그는 항상 당신에게 ''부장님이 이거 다 확인하셨죠?''라고 물어본다!', '매일 같은 커피를 타며, 반복적으로 문서에 서명하는 삶을 살기.', '신입 직원의 보고를 받기 위해, 매일 부장님의 기분을 체크하고 살금살금 돌아다니기.', '반복업무', '강한위계질서', '2026-05-27 03:22:56.661959+00');
INSERT INTO public.ai_generated_scenarios VALUES (7, 6, 10, '혼자서의 대화', '당신은 우주 먼지로 가득한 사무실에 혼자 남겨져, 컴퓨터와 대화하며 하루를 보내고 있습니다. 하지만 이 컴퓨터는 전기세를 아끼기 위해 오프라인 모드에서만 작동합니다!', '혼자서 10시간을 묵묵히 컴퓨터와 대화하기.', '상사가 하루 종일 ''지시''만 하는 상황에서 일하기.', '고독', '권위', '2026-05-27 03:23:21.174246+00');
INSERT INTO public.ai_generated_scenarios VALUES (8, 8, 6, '불가능한 양배추 전쟁', '양배추를 소중히 여기는 마을에서, 당신은 양배추 수확 책임자가 되었다. 하지만 마을 사람들이 당신의 양배추를 훔쳐가고, 당신은 매일 밤마다 양배추를 지키기 위해 전투를 벌여야 한다.', '마을 사람들과의 전투를 마치고 양배추를 지키는 책임을 느끼는 것.', '혼자서 밤새 양배추를 지키는 외로운 감정에 시달리는 것.', '책임감', '고독', '2026-05-27 03:24:00.919331+00');
INSERT INTO public.ai_generated_scenarios VALUES (9, 7, 8, '팀워크의 악몽', '당신은 고양이 피라미드를 쌓는 팀 프로젝트에 배정되었습니다. 그런데 팀원 모두가 고양이 대신 생선으로 피라미드를 쌓고 싶어 합니다!', '팀원들과 생선으로 피라미드를 쌓아야 하는 상황에서 협업의 끝을 느껴보세요.', '생선을 원한 팀원들이 내놓은 계획이 실패하면 당신이 모든 고양이의 책임을 져야 합니다.', '협업', '책임감', '2026-05-27 03:24:38.345221+00');
INSERT INTO public.ai_generated_scenarios VALUES (10, 1, 3, '야근 VS 대인관계', '한밤중, 커피 머신이 고장 나면 어떻게 될까? 당신은 시계가 12시를 지나도 사무실에서 홀로 남아, 스스로를 ''근무의 늪''에 빠뜨린 채 문서 정리를 하고 있다. 아니면, 연속으로 끊임없이 전화가 울리며 ''고객님, 저희는 당신의 목소리를 듣고 싶습니다!''라고 외치는 소리에 시달리는 중이다.', '혼자 사무실에서 야근하며, 커피를 따르는 대신 눈물의 바다를 만들어낸다.', '전화를 받으며, 끊임없이 같은 질문을 반복해야 하는 고객의 열정에 기절할 것 같다.', '야근', '대인관계', '2026-05-27 03:24:51.905432+00');
INSERT INTO public.ai_generated_scenarios VALUES (11, 7, 4, '신입사원의 하루', '당신은 신입사원으로 환영받는 첫날, 팀원들이 모두 페인트를 칠하고 있습니다. 하지만 이상하게도 그들은 ''더 많은 팀워크''를 위해 서로의 얼굴에 페인트를 덕지덕지 바르기 시작했습니다.', '팀워크를 위해 얼굴에 페인트칠 당하기.', '문서 작업 중 갑자기 외근을 가자고 소리치는 상사의 호출에 달려나가기.', '팀협업', '외근많음', '2026-05-27 03:59:57.938831+00');
INSERT INTO public.ai_generated_scenarios VALUES (12, 5, 3, '로봇 청소기와의 전쟁', '너는 로봇 청소기와 함께 청소를 해야 하는데, 이놈의 센서가 맨날 너의 발을 쳐서 몸이 아프다! 그런데 갑자기 로봇 청소기가 ''사랑해요''라고 외치며 너를 쫓아오기 시작했다.', '로봇 청소기에게 발목 잡혀서 2시간 동안 청소하기.', '청소기에게 짜증내며 2시간 동안 고객 서비스 전화 응대하기.', '육체노동', '대인응대', '2026-05-27 04:00:17.481128+00');
INSERT INTO public.ai_generated_scenarios VALUES (13, 1, 2, '야근의 유혹과 반복의 덫', '어둠 속에서 홀로 남겨진 당신, 컴퓨터 화면의 빛은 마치 외계인이 당신을 뜻밖에 채찍질하는 것처럼 아프다. 한편, 매일 같은 문서를 복사해 내는 드라이기 소리는 귀찮음의 최고봉을 찍으며 당신의 귀에 쉴 새 없이 맴돈다.', '끝이 보이지 않는 야근의 연속, 매일 밤 10시를 지나도 집에 갈 수 없다.', '매일 똑같은 문서를 100번 복사하며 복사기는 당신의 가장 친한 친구가 된다.', '야근', '반복', '2026-05-27 04:00:39.52608+00');
INSERT INTO public.ai_generated_scenarios VALUES (14, 3, 10, '상사와의 불꽃 싸움', '당신은 회사에서 외국인 상사와의 1대1 회의에 잡혔습니다. 하지만 그 상사는 이탈리아 배추 요리 전문가로, 당신의 의견을 듣기보단 배추의 역사에 대해 3시간 동안 설명하고 있습니다.', '그를 끊고 배추 대신 당신의 의견을 이야기할 것인가?', '그의 긴 이야기를 끝까지 들으며 고개를 숙일 것인가?', '대인응대', '위계질서', '2026-05-27 04:01:00.447842+00');
INSERT INTO public.ai_generated_scenarios VALUES (15, 7, 5, '팀워크 VS 힘든 일', '너는 신비한 빵집에서 일하게 되었는데, 매일 매일 한 팀원과 함께 ''환상의 크림빵''을 만들기 위해 끊임없이 의견을 맞춰야 해. 그런데 그 팀원은 크림 대신 고추장을 선호하는 이상한 사람이라 너는 지금 갈등의 한가운데에 빠져있어!', '매일 고추장으로 빵을 만들기 위해 팀원과 싸워야 하는 상황.', '한 여름날, 1톤의 밀가루를 힘들게 옮기고 있는데, 마법의 밀가루 요정이 다가와 밀가루를 뿌려대는 상황.', '협업', '육체노동', '2026-05-27 04:01:52.603349+00');
INSERT INTO public.ai_generated_scenarios VALUES (16, 5, 1, '정신없는 대청소', '할아버지의 집에서 3일 동안 쌓인 쓰레기를 정리하는 미션이 주어졌다. 쓰레기를 정리하다보니 갑자기 할아버지가 ''이거 다 내 젊은 시절의 꿈이야''라고 외치며 구석에 쳐박힌 유리병을 들고 달려온다!', '온몸이 아프도록 쓰레기를 옮기고 싶다.', '할아버지의 꿈을 들으며 밤을 꼬박 세우고 싶다.', '육체노동', '야근', '2026-05-27 04:02:15.033135+00');
INSERT INTO public.ai_generated_scenarios VALUES (17, 9, 1, '무한 상상력 대결', '무지개 나라의 왕이 당신에게 기발한 아이디어를 요구합니다. 당신은 매일매일 새로운 상상을 해야 하는데, 오늘은 ''초콜릿으로 만든 비행기''를 떠올려야 합니다! 하지만, 이 아이디어가 맘에 안 드는 왕이 또 다른 상상을 강요하면 어떻게 할까요?', '상상력이 바닥나기 전까지 초콜릿 비행기를 디자인하며 머리가 아픈 걸 선택하세요.', '결국 야근을 하며 초콜릿 비행기를 만드는 대신, 왕의 누군가를 소환해 덤벼들이는 고통을 선택하세요.', '창의성', '야근', '2026-05-27 04:09:20.873988+00');
INSERT INTO public.ai_generated_scenarios VALUES (18, 4, 8, '길을 잃은 외근맨', '토끼 모양의 점퍼를 입고 외근 중인 당신은 갑자기 GPS가 고장 나더니, 끝없이 이어지는 공사 구역에서 길을 잃었습니다. 무려 3시간 이상을 방황한 끝에 발견한 것은 ''전국 민속놀이 대회'' 현장이었고, 당신은 신발을 신고 전통 춤을 추게 됩니다!', '아무도 없는 공공장소에서 무작정 배회하는 외근의 고통.', '이 춤을 추면 무려 5천명의 관중 앞에서 ''사장님이 졸라무서운 기획 발표''를 해야 하는 부담.', '외근', '책임감', '2026-05-27 04:09:29.448817+00');
INSERT INTO public.ai_generated_scenarios VALUES (19, 4, 2, '지옥의 출장과 사무실', '당신은 오늘도 불타는 태양 아래에서 사무실로 돌아가기 위해 발로 빠진 고구마를 쫓고 있습니다. 하지만 사무실에서 기다리는 것은 매일 같은 보고서 작성과 열대야의 반복입니다.', '한여름에 하루 종일 외근하며 얼음물로 시원하게 몸을 식힌다고 상상해보세요.', '사무실에서 매일 같은 문서의 복사본을 100장씩 출력하며, ''안녕하세요''라고 인사하는 복사 기계의 소음에 시달린다고 해보세요.', '외근많음', '반복업무', '2026-05-27 04:09:35.711309+00');
INSERT INTO public.ai_generated_scenarios VALUES (20, 4, 10, '택시 대소동', '택시를 타고 외근을 다니던 당신, 갑자기 기사님이 ''길이 막혀서 해적선으로 가야겠다''고 선언합니다. 해적선에서 일을 하면서도 외근이 끊이질 않아, 해적과 함께 신비한 섬으로 향하고 있습니다.', '해적선에서 기한 맞추려고 외근을 계속해야 한다.', '선장님의 기분에 따라 언제든 명령이 떨어지는 강한 계급 사회에서 일해야 한다.', '외근많음', '위계질서', '2026-05-27 04:09:40.695564+00');
INSERT INTO public.ai_generated_scenarios VALUES (21, 10, 5, '상사와의 불편한 동행', '당신은 무거운 재활용 통을 끌고 가는 푸른 유니폼을 입은 청소부입니다. 그때, 공원에서 당신의 상사가 다가와 ''내가 청소하는 방법을 알려줄 테니, 나를 따라와!''라고 외칩니다.', '상사와 함께 팀워크를 외치며 한없이 위계질서를 따르기.', '재활용 통을 끌며 끊임없이 땀을 흘리는 육체 노동.', '위계질서', '육체노동', '2026-05-27 04:09:45.950478+00');
INSERT INTO public.ai_generated_scenarios VALUES (22, 2, 7, '무한 반복의 미로', '당신은 이제 매일같이 같은 표정으로 ''사과''와 ''배''를 그리는 대형 과일 회사의 직원이 되었습니다. 하루 종일 같은 과일을 그리며, 당신의 영혼은 점점 딱딱해지고 있습니다.', '직원들과 소통도 없이 혼자서 무한히 과일을 그리며, 마음속에서 프리랜서의 꿈이 사라지는 것이 더 싫다.', '매일 아침 팀원들과 함께 과일을 그리며, ''사과는 이렇게 그려야 해!''라고 외치는 팀장의 목소리가 더 싫다.', '반복업무', '팀협업', '2026-05-27 12:06:04.563025+00');
INSERT INTO public.ai_generated_scenarios VALUES (23, 7, 10, '팀워크의 악몽', '당신은 팀 프로젝트 중 서로의 의견이 대립하여 피자 토핑을 놓고 3시간 동안 대치하는 상황에 놓였습니다. 그 사이 피자는 차가워지고, 심지어 한 팀원이 스스로를 ''피자 주술사''라고 주장하기 시작합니다.', '팀원들이 ''피자 주술사''를 존중하라고 강요하며, 당신의 의견을 완전히 무시하는 걸 더 싫어하나요?', '상사에게 ''꼴불견 피자 토핑''이라고 지목당하고, 그로 인해 매일 매일 피자를 회의에 들고 오도록 강요받는 걸 더 싫어하나요?', '협업', '위계질서', '2026-05-27 12:06:24.853582+00');
INSERT INTO public.ai_generated_scenarios VALUES (24, 7, 6, '팀워크의 마법', '당신은 팀 프로젝트 중 한 명이 이상한 마법에 걸려 ''모두의 의견을 들어야만 한다''는 저주에 시달리고 있습니다. 매일 매일 회의에서 아이디어를 제시하지만, 팀원들은 각자 자신의 강아지 이름을 말하는 데만 집중하고 있습니다!', '모두 함께 강아지 이름을 맞추기 위해 3시간 동안 토론하기.', '혼자서 강아지 이름 100개를 외우며 24시간 동안 방에 갇히기.', '협업', '혼자', '2026-05-27 12:06:28.664002+00');
INSERT INTO public.ai_generated_scenarios VALUES (25, 8, 5, '책임감과 근육의 대결', '당신은 회사의 회의실에서 열띤 논쟁 중, CEO가 당신에게 ''이 프로젝트를 제발 성공시키라''며 눈에서 불이 나고 있습니다. 한편, 옆에서는 담당 팀원들이 서로의 머리를 부여잡고 육체적으로 싸우기 시작합니다.', 'CEO의 눈빛을 견디며 책임감을 느끼기.', '팀원들의 격렬한 싸움에 끼어들며 육체적으로 흥분하기.', '책임감', '노동', '2026-05-27 12:06:36.313027+00');
INSERT INTO public.ai_generated_scenarios VALUES (26, 10, 9, '위계와 창의의 대결', '당신은 점심시간에 ''가장 위대한 부장님''이 되어야 하는 미친 사무실에서 일하고 있습니다. 매번 부장님이 드리운 ''비밀 지시''를 따라야 하지만, 오늘은 상사가 고양이 모양의 보고서를 요구하고 있습니다!', '부장님이 지시한 대로 고양이 보고서를 10시간 동안 반복해서 수정해야 한다.', '상사의 창의적인 요구에 맞춰 매일 새로운 고양이 레시피를 개발해야 한다.', '위계질서', '창의성', '2026-05-27 12:06:40.087006+00');
INSERT INTO public.ai_generated_scenarios VALUES (27, 2, 6, '사무실의 고통', '상상해보세요, 매일 아침 같은 보고서를 줄 세워 복사하는 일을 맡게 된 당신! 그리고 발 밑에는 늘 배고픈 고양이가 있어, 배가 고플 때마다 그 고양이의 눈빛이 당신을 압박합니다.', '하루 종일 똑같은 보고서를 복사하는 일과 고양이의 시선, 어느 쪽이 더 괴롭겠나요?', '옆자리에 말도 안 되는 소리만 하는 동료가 있지만, 혼자서 아무도 없는 사무실에서 발리볼 서류봉투와 대화해야 한다면?', '반복업무', '혼자일하기', '2026-05-27 12:17:18.86508+00');
INSERT INTO public.ai_generated_scenarios VALUES (28, 9, 3, '직업 세계의 두 얼굴', '어느 날 당신은 직업 상담을 받기 위해 ''이상한 직업학교''에 들어갔습니다. 그곳에서 한 인간형 로봇이 당신에게 각기 다른 두 가지 직업 경험을 제안하는데, 하나는 상상 이상의 창의력을 요구하고 다른 하나는 미소를 잃지 말라는 압박을 줍니다.', '매일 아침 캔버스에 제 몸을 던지며 신선한 아이디어를 짜내야 한다는 압박감!', '하루 종일 사람들과 이야기를 나누면서도 내 기분이 어떻든지 항상 웃음을 지켜야 한다는 고통!', '창의성', '대인관계', '2026-05-27 12:17:41.638465+00');
INSERT INTO public.ai_generated_scenarios VALUES (29, 10, 8, '상사 VS 팀원', '당신은 갑자기 ''우주 대전문서''라는 프로젝트의 팀장이 되었고, 모든 결정은 상사의 리뷰를 거쳐야 한다! 그런데 상사는 매일 아침 7시 회의를 위해 고양이 복장을 하고 나타난다.', '매일 고양이 복장으로 회의하는 상사의 눈치를 보며, 팀원들에게 비밀번호를 묻는 일.', '상사가 지나치게 심각하게 ''우주 대전''의 성공에 대해 압박하며, 그 책임을 혼자 지는 일.', '위계질서', '책임감', '2026-05-27 12:17:58.381744+00');
INSERT INTO public.ai_generated_scenarios VALUES (30, 2, 5, '사무실의 미친 반복', '매일 아침, 당신은 사무실에서 끝없이 같은 파일을 복사하고 붙여넣는 지옥 같은 반복 업무에 갇혔습니다. 그러던 어느 날, 사무실에 갑자기 나타난 괴물 같은 청소부가 당신의 복사본을 한 장씩 찢어버리기 시작합니다!', '그 괴물이 당신의 사무실에서 복사한 모든 파일을 찢어버리는 걸 지켜본다.', '그 괴물이 사무실 청소를 하며 당신의 머리 위로 무거운 청소기 통을 옮기는 걸 피해야 한다.', '반복업무', '육체노동', '2026-05-27 12:18:16.874306+00');
INSERT INTO public.ai_generated_scenarios VALUES (31, 5, 9, '가상의 하루 일과', '당신은 어제 불꽃놀이를 너무 가까이서 관람하다가 스파클링 폭죽에 치여서, 오늘 아침은 부엌에서 일어나는 불꽃놀이를 수습해야 합니다. 부엌이 폭발적인 상황이라, 리모컨을 들고 있는 고양이까지 동참했어요!', '부엌 바닥에 쏟아진 스파클링 소스를 12시간 동안 청소하는 것.', '매일 아침, 고양이를 위해 새로운 레시피로 불꽃놀이 쿠키를 창조해야 하는 것.', '육체노동', '창의성', '2026-05-27 12:18:25.204459+00');
INSERT INTO public.ai_generated_scenarios VALUES (32, 2, 9, '무한 텀블러 대작전', '매일 아침 출근길에 같은 커피숍에서 100개의 텀블러를 비우는 임무를 맡은 당신. 매일 반복해서 같은 커피 맛을 경험하는 건 괴로운 일이다. 그런데 오늘은 그 커피숍이 ''사계절 커피''로 시즌 한정 메뉴를 바꿔버렸다!', '매일 똑같은 커피를 마시며 반복하는 지루함을 견뎌낼 것인가?', '시즌 한정 메뉴를 위해 창의력 대결을 벌여야 하는데, 심지어 블라인드 테스트로 세 가지 맛 중 하나를 고르는 미션을 수행해야 할 것인가?', '지루함', '창의성', '2026-05-27 13:02:57.461999+00');
INSERT INTO public.ai_generated_scenarios VALUES (65, 1, 7, '밤샘 회의의 마법', '당신은 한밤중에 갑자기 회사에 소환된 마법사입니다. 마법의 주문이 잘못되어 동료들이 양파처럼 울면서 보고서를 쓰고 있는데, 당신은 이 상황에서 도망칠 수 없습니다.', '주문을 외우며 밤새도록 야근하는 게 더 싫어요.', '동료들의 눈물 속에서 팀워크를 강요받는 게 더 싫어요.', '야근', '팀워크', '2026-05-27 13:06:39.699994+00');
INSERT INTO public.ai_generated_scenarios VALUES (66, 1, 6, '야근 vs. 혼자 일하기', '퇴근 시간이 지나고, 갑자기 회사에 마법사가 나타나 ''야근 마법''을 걸어버린다! 마법의 힘으로 직원들은 저녁 9시까지 회의를 하며 피자와 콜라를 단체로 시켜야 한다.', '마법사에게 ''이걸 더 하라''고 강요받으며 밤새도록 회의록을 작성해야 한다.', '혼자서 피자를 먹으며 마법사가 은밀히 직원이라며 할 일 목록을 보내는 바람에, 1시간마다 혼자서 그들을 위한 보고서를 작성해야 한다.', '야근', '혼자', '2026-05-27 13:17:43.851707+00');
INSERT INTO public.ai_generated_scenarios VALUES (67, 9, 4, '색깔이 없는 사무실', '당신은 초능력으로 색깔 없는 세상을 구하는 미술가입니다. 하지만 당신의 스튜디오는 매일 같은 회색 벽으로 둘러싸여 있어 창의력이 고갈되고, 사무실에 붙은 스티커들로 세상이 몽환적으로 엉망이 되어버렸죠.', '매일 똑같은 회의에서 ''창의적 아이디어''를 강요당하는 것은 정말 최악입니다.', '매일 외근으로 나가 동네 식당의 메뉴를 조사하는 것도 참을 수 없는 고통입니다.', '창의성', '외근', '2026-05-27 13:17:50.870894+00');
INSERT INTO public.ai_generated_scenarios VALUES (68, 4, 5, '출근길 괴담', '한 여름 날씨에 너는 외근 중이야. 회사에서 요청한 서류를 전달하기 위해 눈부신 태양 아래 10킬로미터를 걸어야 하는데, 갈증이 심해 물통을 잊어버린 걸 깨달았어!', '내일도 이 길을 걸어야 한다면, 더 싫은 건 그 햇빛 아래 계속 돌아다니는 거야.', '혹시라도 회사에서 시키는 짐을 들고 다녀야 한다면, 더 싫은 건 그 무거운 박스를 하루 종일 옮기는 거야.', '외근많음', '육체노동', '2026-05-27 13:17:57.669606+00');
INSERT INTO public.ai_generated_scenarios VALUES (69, 8, 3, '벌레와 소통하는 하루', '당신은 오늘 벌레들과 한 팀이 되어 일해야 합니다. 한쪽은 벌레의 리더 역할을 맡고, 다른 쪽은 벌레들에게 직접 명령을 내리며 소통해야 합니다. 벌레들이 당신의 착한 의도를 알아주기만을 바라는 하루!', '벌레들이 당신의 임무를 제대로 수행하지 않으면, 당신이 그 결과를 책임져야 합니다.', '벌레와 대화하며 생기는 오해로 인해, 계속해서 그들에게 사과하고 설명해야 합니다.', '책임감', '대인응대', '2026-05-27 13:18:05.064535+00');
INSERT INTO public.ai_generated_scenarios VALUES (70, 6, 9, '혼자서 떠나는 여행', '혼자서 누군가의 생일 파티에 갔는데, 초대받은 모든 사람이 자아 성찰을 위해 ''혼자''로 축제를 즐기는 이벤트를 열었다. 주인공은 스스로 ''혼자''의 의미를 깨닫기 위해, 무한히 목소리를 내며 혼잣말을 해야 한다!', '한쪽 구석에서 고요하게 혼자 앉아, 심지어 스스로에게 ''고기 들어간 김밥''이 무엇인지 물어봐야 한다.', '매 순간 창의적인 축하 메시지를 만들어야 하며, 초대받지 않은 초능력 생명체에게도 재치있게 말해야 한다.', '고독', '창의성', '2026-05-27 13:18:11.029495+00');


--
-- Data for Name: balance_scenarios; Type: TABLE DATA; Schema: public; Owner: careernobox
--



--
-- Data for Name: balance_choices; Type: TABLE DATA; Schema: public; Owner: careernobox
--



--
-- Data for Name: companies; Type: TABLE DATA; Schema: public; Owner: careernobox
--



--
-- Data for Name: company_blacklists; Type: TABLE DATA; Schema: public; Owner: careernobox
--



--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: careernobox
--

INSERT INTO public.users VALUES (1, '0sunghee122@gmail.com', '$2b$12$uJwDWIjwbMeKTxe9vwMW7OdqlITLjDRG6C3PZ024XMpCaK5Gg/abS', true, false, '2026-05-27 02:33:44.594553+00', '2026-05-27 02:33:44.594553+00');


--
-- Data for Name: company_reviews; Type: TABLE DATA; Schema: public; Owner: careernobox
--



--
-- Data for Name: company_warning_tags; Type: TABLE DATA; Schema: public; Owner: careernobox
--



--
-- Data for Name: face_readings; Type: TABLE DATA; Schema: public; Owner: careernobox
--



--
-- Data for Name: fortune_reports; Type: TABLE DATA; Schema: public; Owner: careernobox
--



--
-- Data for Name: report_logs; Type: TABLE DATA; Schema: public; Owner: careernobox
--



--
-- Data for Name: user_profiles; Type: TABLE DATA; Schema: public; Owner: careernobox
--



--
-- Data for Name: user_awards; Type: TABLE DATA; Schema: public; Owner: careernobox
--



--
-- Data for Name: user_balance_answers; Type: TABLE DATA; Schema: public; Owner: careernobox
--



--
-- Data for Name: user_certifications; Type: TABLE DATA; Schema: public; Owner: careernobox
--



--
-- Data for Name: user_fear_tags; Type: TABLE DATA; Schema: public; Owner: careernobox
--

INSERT INTO public.user_fear_tags VALUES (3, 1, 2, 1.2, '2026-05-27 03:18:54.115233+00', false);
INSERT INTO public.user_fear_tags VALUES (7, 1, 3, 3.9000000000000004, '2026-05-27 04:01:52.089455+00', false);
INSERT INTO public.user_fear_tags VALUES (6, 1, 7, 5, '2026-05-27 12:06:35.800006+00', false);
INSERT INTO public.user_fear_tags VALUES (5, 1, 6, 3, '2026-05-27 12:17:41.104428+00', false);
INSERT INTO public.user_fear_tags VALUES (2, 1, 1, 4.5, '2026-05-27 13:17:50.349009+00', false);
INSERT INTO public.user_fear_tags VALUES (10, 1, 4, 4, '2026-05-27 13:18:04.534589+00', false);
INSERT INTO public.user_fear_tags VALUES (9, 1, 8, 3.9000000000000004, '2026-05-27 13:18:29.252656+00', false);
INSERT INTO public.user_fear_tags VALUES (4, 1, 9, 5.5, '2026-05-27 13:18:29.701174+00', false);
INSERT INTO public.user_fear_tags VALUES (8, 1, 5, 6, '2026-05-27 13:35:10.634707+00', false);
INSERT INTO public.user_fear_tags VALUES (1, 1, 10, 7.2, '2026-05-27 13:35:15.752649+00', true);


--
-- Data for Name: user_scores; Type: TABLE DATA; Schema: public; Owner: careernobox
--



--
-- Name: ai_generated_scenarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.ai_generated_scenarios_id_seq', 70, true);


--
-- Name: balance_choices_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.balance_choices_id_seq', 1, false);


--
-- Name: balance_scenarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.balance_scenarios_id_seq', 1, false);


--
-- Name: companies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.companies_id_seq', 1, false);


--
-- Name: company_blacklists_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.company_blacklists_id_seq', 1, false);


--
-- Name: company_reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.company_reviews_id_seq', 1, false);


--
-- Name: company_warning_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.company_warning_tags_id_seq', 1, false);


--
-- Name: face_readings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.face_readings_id_seq', 1, false);


--
-- Name: fear_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.fear_tags_id_seq', 10, true);


--
-- Name: fortune_reports_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.fortune_reports_id_seq', 1, false);


--
-- Name: report_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.report_logs_id_seq', 1, false);


--
-- Name: user_awards_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.user_awards_id_seq', 1, false);


--
-- Name: user_balance_answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.user_balance_answers_id_seq', 1, false);


--
-- Name: user_certifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.user_certifications_id_seq', 1, false);


--
-- Name: user_fear_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.user_fear_tags_id_seq', 10, true);


--
-- Name: user_profiles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.user_profiles_id_seq', 1, false);


--
-- Name: user_scores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.user_scores_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: careernobox
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

\unrestrict hIpmqg5TVp09eMS445ZQFmCcYYuZTu3IQ6KcjApfc3Yrzm8qRp5SlPdycSgEP1Y

