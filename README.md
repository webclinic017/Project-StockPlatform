## Investment Simulation Platform
증권API,크롤링으로 얻은 주가 데이터를 유저의 투자전략에 따라 시뮬레이션 해 봄으로써 투자에 도움을 주는 플랫폼입니다. 

1. 사용자가 매수, 매도의 기준을 직접 설정합니다.
- 매출액, 영업이익, 주가, 시가총액, PER, PBR, ROE, 현금흐름, 부채 비율 등의 지표가 있습니다. 
- 사용자가 주도적으로 매수, 매도 기준을 설정합니다. 

2. 백테스팅 서비스를 제공합니다. 
- 특정 기간을 설정하고, 사용자가 선택한 전략대로 과거 시뮬레이션을 진행합니다. 
- 과거 주가 데이터를 활용하여 불확실성을 줄이고, 자신만의 투자 전략을 수립합니다. 
- 실제처럼 실행하고 모든 결과를 기록해 분석합니다. 
- 전략의 성과를 평가합니다. 

3. 플랫폼 자체 커뮤니티로 투자자간 정보 공유 서비스를 제공합니다.
- 자신의 전략에 대한 다른 사람의 의견을 듣기 위해 백테스팅 데이터를 커뮤니티에 공유할 수 있습니다. 
- 커뮤니티에서 의견을 주고받으며 투자에 관한 다양한 지식을 쌓을 수 있습니다. 또한, 전략을 평가받고 부족한 것이나 잘못된 것을 고칠 수 있습니다.
- 백테스팅으로 구한 수익률 데이터를, 다양한 측면을 반영한 수치로 분석하여 나에게 적합한 전략인지 아닌지 판가름 해줍니다. 

## Tech/framework used
- Framework : Django3.0, Django-Rest-Framework
- Language : python3.8(32/64), javascript
- OS : Ubuntu 18.0.4
- DB : MongoDB Atlas
- Cloud : AWS-EC2

## Data flow
<img src="https://github.com/Seungyeup/Project-StockPlatform/blob/master/imgs/%EC%A0%84%EA%B0%9C%EB%8F%84%201.png?raw=true"  width="70%" height="70%">

## Data flow(Detail)
![intro page3](https://github.com/Seungyeup/Project-StockPlatform/blob/master/imgs/%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD3.png?raw=true)

## License
A short snippet describing the license (MIT, Apache etc)

MIT © [Yourname]()
