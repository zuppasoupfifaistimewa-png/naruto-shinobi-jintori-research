# AZ1 — catatan rekonsiliasi run2 yang lebih lama
Tanggal: 2 November 2026
Run 41359528784, Job ID 125006729967, Source SHA 6c1e3b95e54ebfa46468e62b96cd0cd08d85ab9a, H6 HYBRID d57b626100d1023e8f63ec2c7d559bffcfd152453b1affc36032c1d642ee3475.

Run tersebut mencapture dua launch × frame180/360. Snapshot yang diparse telah ditulis ke manager/tile/table/aggregate TSV sebelum exception pada return akhir read_snapshot (NameError: row). Oleh sebab itu script exit code desimal 2 dan Actions report tetap INCOMPLETE; run tersebut tidak boleh dilabel PASS. AZ1_LAUNCHES_RECONCILED.tsv menggabungkan RAM SHA dari AZ1_MANAGER_FIELDS dengan exit code, waktu dan SHA Memory Card dari launch log; rekonsiliasi ini adalah bukti sekunder, bukan pengganti summary PASS.

**Run4 41360900093** memperbaiki semua return, lebar state menjadi u8, dan menyelesaikan keempat snapshot dengan Actions PASS/script exit 0. Gunakan AZ1_FINAL_RUNTIME_REPORT_2026-11-02.md dan output run4 sebagai bukti final K5-H6. Run2 dipertahankan hanya sebagai jejak audit kesalahan parser yang sudah diperbaiki.
