## WSL 사용자 설치 방법

### 1. WSL 내부에서 Git 설치 확인

```bash
git --version

명령어를 찾을 수 없다면:

sudo apt update
sudo apt install git
2. WSL 홈 디렉터리에서 clone

Windows의 /mnt/c/... 경로보다 WSL Linux 홈 디렉터리 사용을 권장합니다.

cd ~
pwd

예:

/home/<username>

Repository clone:

git clone https://github.com/sbeetle1003-stack/team2.git
cd team2
3. 원격 branch 확인
git branch -a

다음 branch가 보여야 합니다.

remotes/origin/feature/active-vision

보이지 않는다면:

git fetch origin
git branch -a
4. Active Vision branch로 이동
git switch feature/active-vision

만약 다음과 같이 branch를 찾을 수 없다는 오류가 발생하면:

fatal: invalid reference: feature/active-vision

다음 명령을 사용합니다.

git switch -c feature/active-vision --track origin/feature/active-vision

또는 처음부터 해당 branch만 clone할 수 있습니다.

cd ~

git clone \
  --branch feature/active-vision \
  https://github.com/sbeetle1003-stack/team2.git

cd team2

GitHub에서 `git clone`을 하면 원격 branch 정보도 로컬의 `origin/...` remote-tracking branch로 내려받고, `git fetch`로 새 원격 branch를 갱신할 수 있어. :contentReference[oaicite:1]{index=1}

특히 팀원이 **`git switch feature/active-vision`에서 막힌다면**, 가장 먼저 이걸 확인하면 돼.

```bash
cd ~/team2

git remote -v
git branch -a

정상이라면:

origin  https://github.com/sbeetle1003-stack/team2.git (fetch)
origin  https://github.com/sbeetle1003-stack/team2.git (push)

* main
  remotes/origin/main
  remotes/origin/feature/active-vision

처럼 보여야 해.

remotes/origin/feature/active-vision이 있는데 git switch feature/active-vision이 안 된다면:

git switch --track origin/feature/active-vision

이면 돼.
