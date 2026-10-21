# CXJ - Extração remota ADSB.lol (piloto)

1. Crie um repositório no GitHub, preferencialmente privado.
2. Coloque `.github/workflows/extract-adsb.yml` e `scripts/extract.py` mantendo as pastas.
3. Vá em **Actions > CXJ - Extrair ADSB.lol > Run workflow**.
4. Defina `2026-06-29`, `e494b4`, `prod`. Execute.
5. Após a execução, baixe o artefato `cxj-adsb-2026-06-29` e compartilhe os arquivos produzidos para nossa auditoria.

O runner recebe remotamente todas as partes TAR do dia (vários GB de tráfego), **sem transferi-las para seu computador**. O script lê o TAR em fluxo, sem salvar a íntegra, e retém apenas arquivos cujo nome contenha o ICAO24 pedido. O artefato pode estar vazio se não houver registro para essa aeronave ou cobertura na data. Isso não comprova ausência de decolagem.

Se a tarefa não concluir, verificar os logs: downloads públicos podem falhar por tamanho, rede, limites do runner, expiração ou restrições de tráfego GitHub. Os pacotes TAR também podem ter arquivos em formatos/nomes diferentes; nesse caso ajustar o filtro após conferir uma listagem. Esta é uma versão piloto, não verificada contra um TAR real de 2026.

Fonte: https://github.com/adsblol/globe_history_2026 ; crédito ADSB.lol, dados ODbL.
