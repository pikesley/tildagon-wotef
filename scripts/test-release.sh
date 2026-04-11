TAG=$(uuidgen)
APP=$(basename $(pwd))
OUTDIR=/tmp/${APP}

rm -fr ${OUTDIR}
mkdir -p ${OUTDIR}

git tag ${TAG}

git archive --format tar --prefix ${APP}/ ${TAG} > ${OUTDIR}/rc.tar

cd ${OUTDIR}

tar xvf rc.tar

cd wotef
python -m mpremote fs mkdir :/apps/wotef
python -m mpremote fs cp -r * :/apps/wotef
