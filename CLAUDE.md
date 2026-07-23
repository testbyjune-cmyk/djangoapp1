# CLAUDE.md

이 저장소에서 작업할 때 아래 원칙을 반드시 따른다.

## 1. SOLID 원칙

모든 소스 코드는 SOLID 원칙을 지켜서 작성한다.

- **S (단일 책임 원칙)**: 클래스/모듈/함수는 하나의 책임만 가진다. 변경 이유가 하나여야 한다.
- **O (개방-폐쇄 원칙)**: 확장에는 열려 있고 수정에는 닫혀 있어야 한다. 기존 코드를 고치지 않고 새 기능을 추가할 수 있는 구조로 설계한다.
- **L (리스코프 치환 원칙)**: 하위 타입은 상위 타입을 대체할 수 있어야 하며, 상위 타입의 계약을 깨서는 안 된다.
- **I (인터페이스 분리 원칙)**: 클라이언트가 사용하지 않는 인터페이스에 의존하지 않도록 인터페이스를 최소 단위로 분리한다.
- **D (의존관계 역전 원칙)**: 상위 모듈이 하위 모듈의 구체 구현이 아니라 추상화(인터페이스)에 의존하도록 설계한다.

## 2. UX/UI — 닐슨 10가지 사용성 원칙

모든 UX/UI 작업은 Jakob Nielsen의 10가지 사용성 휴리스틱을 따른다.

1. 시스템 상태의 가시성 (Visibility of system status)
2. 시스템과 현실 세계의 일치 (Match between system and the real world)
3. 사용자 제어와 자유 (User control and freedom)
4. 일관성과 표준 (Consistency and standards)
5. 오류 예방 (Error prevention)
6. 기억보다 인지 (Recognition rather than recall)
7. 사용 유연성과 효율성 (Flexibility and efficiency of use)
8. 미학적이고 미니멀한 디자인 (Aesthetic and minimalist design)
9. 오류 인식, 진단, 복구 지원 (Help users recognize, diagnose, and recover from errors)
10. 도움말 및 문서 제공 (Help and documentation)

## 3. 플러그인 구조

향후 확장 및 수정이 용이하도록 플러그인(plug-in) 구조를 지킨다.

- 핵심 로직과 확장 기능(플러그인)을 명확히 분리한다.
- 새로운 기능은 핵심 코드를 수정하지 않고 플러그인 형태로 추가할 수 있어야 한다.
- 플러그인은 정의된 인터페이스/규약을 통해서만 핵심 시스템과 통신한다.
- 플러그인 간 직접 의존을 피하고, 핵심 시스템을 통한 느슨한 결합을 유지한다.
