-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 08, 2026 at 01:40 AM
-- Server version: 8.0.30
-- PHP Version: 8.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_surat_rutan`
--

-- --------------------------------------------------------

--
-- Table structure for table `surat`
--

CREATE TABLE `surat` (
  `id` int NOT NULL,
  `jenis` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `judul` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nomor_surat` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tanggal` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT 'Selesai',
  `user_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `surat`
--

INSERT INTO `surat` (`id`, `jenis`, `judul`, `nomor_surat`, `tanggal`, `data`, `status`, `user_id`, `created_at`, `updated_at`) VALUES
(1, 'sptjm', 'SPTJM Perjalanan Dinas', 'UM.01.01.724', '04 April 2026', '{\"nama\": \"Lamhot Sihombing\", \"nip\": \"198503092007031001\", \"pangkat_gol\": \"Penata (III/c)\", \"jabatan\": \"Ka. Pengelolan\", \"nomor_surat\": \"UM.01.01.724\", \"tanggal\": \"04 April 2026\", \"ttd_tempat\": \"Pangkalan Brandan\", \"ttd_tanggal\": \"4 April 2026\", \"ttd_nama\": \"Akmalun Ikhsan\", \"ttd_nip\": \"199702172017123003\", \"mengetahui_nama\": \"\", \"mengetahui_nip\": \"\", \"keterangan\": \"\", \"isi_pernyataan\": \"<ol>\\r\\n\\t<li>Benar telah menjalankan tugas perjalanan dinas berdasarkan Surat Tugas Nomor&nbsp;UM.01.01.724&nbsp;&nbsp;pada tanggal 04 April 2026 tentang Mebersihhkan masjid</li>\\r\\n\\t<li>Benar bahwa biaya perjalanan dinas dari Pangkalan Brandan- Medan yang dibayarkan adalah senilai uang sebesar Rp.500.000</li>\\r\\n</ol>\\r\\n\", \"kegiatan\": \"\", \"biaya_perjalanan\": \"Rp. 3.000.000\", \"biaya_perjalanan_terbilang\": \"Rp. 1.000.000\", \"rute\": \"Pangkalan Brandan- Medan\", \"spd_nomor\": \"655/ST.SPD/2000/10/2026\", \"rincian\": [{\"uraian\": \"Uang Harian\", \"jumlah\": \"Rp. 3.000.000\", \"keterangan\": \"Biaya makan dan kebutuhan selama 3 hari\"}, {\"uraian\": \"Transport\", \"jumlah\": \"Rp. 1.500.000\", \"keterangan\": \"Biaya makan dan kebutuhan selama 3 hari\"}, {\"uraian\": \"Biaya makan dan kebutuhan selama 3 hari\", \"jumlah\": \"Rp. 2.500.000\", \"keterangan\": \"Biaya makan dan kebutuhan selama 3 hari\"}], \"telah_dibayarkan\": \"Rp. 2.000.000\", \"telah_dibayarkan_terbilang\": \"Rp. 2.000.000\", \"bendahara_nama\": \"Imal Pratama Tarigan\", \"bendahara_nip\": \"199702172017121002\", \"penerima_nama\": \"Alief\", \"ditetapkan\": \"Rp. 3.000.000\", \"dibayarkan_semula\": \"Rp. 3.000.000\", \"sisa\": \"Rp. 3.000.000\", \"ppk_nama\": \"Akmalun Ikhsan\", \"ppk_nip\": \"198712252020121001\"}', 'Selesai', 1, '2026-05-04 15:04:42', '2026-05-05 15:23:18'),
(5, 'nota_dinas', 'Nota Dinas', 'A/LHU-KES/BK3-MDN/XII/2025', '04 April 2026', '{\"nama\": \"\", \"nip\": \"\", \"jabatan\": \"\", \"unit_organisasi\": \"\", \"nomor_surat\": \"A/LHU-KES/BK3-MDN/XII/2025\", \"tanggal\": \"04 April 2026\", \"kepada\": \"Bendahara Pengeluaran\", \"hal\": \"Testing\", \"lampiran\": \"Pdf\", \"kegiatan\": \"Bersih-Bersih Masjid\", \"nomor_tugas\": \"UM.10122.22\", \"tanggal_tugas\": \"04 Mei 2026\", \"nominal\": \"3.000.000\", \"isi_pernyataan\": \"Sehubungan dengan telah dilaksanakannya Perjalanan Dinas Sesuai Surat Tugas (Nomor Surat) pada (tanggal) (tentang kegiatan). Bersama ini kami sampaikan pengajuan Pembayaran Perjalanan Dinas Rincian Output   EBD.955 Layanan Manajemen Keuangan Rp.  (Dalam Rupiah) dan telah dilaksanakannya dokumen pertanggungjawaban terkait perjalanan dinas tersebut sebagaimana terlampir, mohon kiranya persetujuan untuk pembayaran kegiatan ini.\\r\\n\\r\\nDemikian disampaikan, atas perhatian dan kehadirannya diucapkan terima kasih.\\r\\n\", \"ttd_tempat\": \"Pangkalan Brandan\", \"ttd_tanggal\": \"4 April 2026\", \"ttd_nama\": \"Akmalun Ikhsan\", \"ttd_nip\": \"199702172017123003\", \"menyetujui_nama\": \"\", \"menyetujui_nip\": \"\", \"keterangan\": \"\"}', 'Selesai', 1, '2026-05-06 07:01:22', '2026-05-06 07:08:17'),
(6, 'laporan_kegiatan', 'Laporan Kegiatan', 'UM.01.01.717', '04 April 2026', '{\"nama\": \"\", \"nip\": \"\", \"jabatan\": \"\", \"unit_organisasi\": \"\", \"nomor_surat\": \"UM.01.01.717\", \"tanggal\": \"04 April 2026\", \"kepada\": \"\", \"hal\": \"\", \"lampiran\": \"\", \"kegiatan\": \"Bersih-Bersih Masjid\", \"nomor_tugas\": \"\", \"tanggal_tugas\": \"\", \"nominal\": \"\", \"isi_pernyataan\": \"\", \"ttd_tempat\": \"Pangkalan Brandan\", \"ttd_tanggal\": \"4 April 2026\", \"ttd_nama\": \"\", \"ttd_nip\": \"\", \"menyetujui_nama\": \"\", \"menyetujui_nip\": \"\", \"keterangan\": \"\", \"nomor_dipa\": \"SP DIPA-135.05.2.692994/2026\", \"tanggal_dipa\": \"12 mei 2026\", \"tempat\": \"Masjid Brandan\", \"uraian_kegiatan\": \"Dalam rangka meningkatkan pemahaman dan kompetensi aparatur di lingkungan Kementerian Imigrasi dan Pemasyarakatan, khususnya dalam bidang pengelolaan administrasi keuangan, telah dilaksanakan kegiatan Pembinaan Administrasi Pengelolaan Hibah Langsung dan Bimbingan Teknis Tata Cara Pembayaran Tunjangan Kinerja.\\r\\n\\r\\nKegiatan ini bertujuan untuk memberikan pemahaman yang komprehensif mengenai mekanisme pengelolaan hibah langsung serta tata cara pembayaran tunjangan kinerja sesuai dengan ketentuan yang berlaku.\\r\\n\\r\\nKegiatan ini diikuti oleh pejabat dan staf dari unit pelaksana teknis di lingkungan Kementerian Imigrasi dan Pemasyarakatan wilayah Sumatera Utara, termasuk perwakilan dari Rutan, Lapas, serta Kantor Imigrasi.\\r\\n\", \"hasil_tindak_lanjut\": \"Terlaksananya Sosialisasi mekanisme pembayaran tunjangan kinerja kepada seluruh operator tunjangan kinerja unit pelaksana teknis Kementerian imigrasi dan pemasyarakatan Sumatera utara\\r\\n\\r\\nDemikian dilaporkan dan diucapkan terima kasih.\\r\\n\", \"petugas\": [{\"nama\": \"THEO KRISTIAN SITOMPUL A.Md. P\", \"nip\": \"199112182016081001\", \"pangkat_gol\": \"Pengatur Tk I (II/d)\", \"jabatan\": \"Kepala Kesatuan Pengamanan Rutan \"}, {\"nama\": \"Rolan Siringo-Ringo\", \"nip\": \"1968080219900732001\", \"pangkat_gol\": \"Penata Tk. I /IIId\", \"jabatan\": \"Ka. Subsi Pelayanan Tahanan \"}], \"pelaksana_nama\": \"Aidina\", \"pelaksana_nip\": \"12052006063001\"}', 'Selesai', 1, '2026-05-06 07:12:43', '2026-05-06 07:13:27'),
(7, 'surat_pernyataan', 'Surat Pernyataan', '', '', '{\"nama\": \"Lamhot Sihombing\", \"nip\": \"1968080219900732001\", \"jabatan\": \"Ka. Subsi Pelayanan Tahanan \", \"unit_organisasi\": \"Imigrasi & Pemasyarakatan\", \"nomor_surat\": \"\", \"tanggal\": \"\", \"kepada\": \"\", \"hal\": \"\", \"lampiran\": \"\", \"kegiatan\": \"\", \"nomor_tugas\": \"\", \"tanggal_tugas\": \"\", \"nominal\": \"\", \"isi_pernyataan\": \"Menyatakan dengan sesunguhnya, bahwa saya telah melaksanakan perjalan dinas kegiatan Studi Tiru WBK Ke Lapas Kelas IIB Majalengka dan Lapas Kelas IIB Sumedang . Selama melaksanakan perjalanan dinas, saya tidak menginap di hotel/tempat penginapan lainnya, dengan demikian biaya penginapan yang saya terima adalah 30% x 686.000 (tarif Hotel di tempat tujuan) x 2 Malam = 410.000\\r\\n\\r\\nDemikian surat pernyataan ini dibuat, untuk dapat dipergunakan sebagaimana mestinya.  \\r\\n\", \"ttd_tempat\": \"Pangkalan Brandan\", \"ttd_tanggal\": \"4 April 2026\", \"ttd_nama\": \"Inal Tarigan\", \"ttd_nip\": \"\", \"menyetujui_nama\": \"Akmalun Ikhsan\", \"menyetujui_nip\": \"\", \"keterangan\": \"\"}', 'Selesai', 1, '2026-05-06 07:16:25', '2026-05-06 07:16:25'),
(8, 'daftar_pengeluaran_rill', 'Daftar Pengeluaran Rill', 'A/LHU-KES/BK3-MDN/XII/2025', '21 April 2026', '{\"nama\": \"Rolan Siringo-Ringo\", \"nip\": \"1968080219900732001\", \"jabatan\": \"Ka. Subsi Pelayanan Tahanan \", \"unit_organisasi\": \"\", \"nomor_surat\": \"A/LHU-KES/BK3-MDN/XII/2025\", \"tanggal\": \"21 April 2026\", \"kepada\": \"\", \"hal\": \"\", \"lampiran\": \"\", \"kegiatan\": \"\", \"nomor_tugas\": \"\", \"tanggal_tugas\": \"\", \"nominal\": \"\", \"isi_pernyataan\": \"\", \"ttd_tempat\": \"Pangkalan Brandan\", \"ttd_tanggal\": \"21 April 2026\", \"ttd_nama\": \"Akmalun Ikhsan\", \"ttd_nip\": \"199702172017123003\", \"menyetujui_nama\": \"\", \"menyetujui_nip\": \"\", \"keterangan\": \"\", \"pengeluaran\": [{\"uraian\": \"Uang Harian\", \"jumlah\": \"5.000.000\"}], \"ppk_nama\": \"\", \"ppk_nip\": \"\"}', 'Selesai', 1, '2026-05-06 07:18:35', '2026-05-06 07:18:35'),
(9, 'sptjm', 'SPTJM Perjalanan Dinas', 'WP.2.PAS.35.KP.04.01-1365', '13 April 2026', '{\"nama\": \"Anwar Arifin\", \"nip\": \"1968080219900732001\", \"jabatan\": \"Operator BMN\", \"unit_organisasi\": \"\", \"nomor_surat\": \"WP.2.PAS.35.KP.04.01-1365\", \"tanggal\": \"13 April 2026\", \"kepada\": \"\", \"hal\": \"\", \"lampiran\": \"\", \"kegiatan\": \"\", \"nomor_tugas\": \"\", \"tanggal_tugas\": \"\", \"nominal\": \"\", \"isi_pernyataan\": \"<p>Pembinaan Administrasi Pengelolaan Hibah Langsung dan Bimbingan Teknis Tata Cara Pembayaran Tunjangan Kinerja</p>\\r\\n\", \"ttd_tempat\": \"Pangkalan Brandan\", \"ttd_tanggal\": \"4 April 2026\", \"ttd_nama\": \"Akmalun Ikhsan\", \"ttd_nip\": \"199702172017123003\", \"menyetujui_nama\": \"\", \"menyetujui_nip\": \"\", \"keterangan\": \"\", \"biaya_perjalanan\": \"Rp.235.000\", \"biaya_perjalanan_terbilang\": \"Dua Ratus Tiga Puluh Lima Ribu Rupiah)\", \"rute\": \"Pangkalan Brandan - Medan\", \"spd_nomor\": \"\", \"rincian\": [{\"uraian\": \"Uang Harian\", \"jumlah\": \"370.000\", \"keterangan\": \"\"}, {\"uraian\": \"Transport\", \"jumlah\": \"372.000\", \"keterangan\": \"\"}], \"telah_dibayarkan\": \"1.000.000\", \"telah_dibayarkan_terbilang\": \"satu juta rupiah\", \"bendahara_nama\": \"Imal Pratama Tarigan\", \"bendahara_nip\": \"199702172017121002\", \"penerima_nama\": \"Fransisco\", \"ditetapkan\": \"Rp. 742.000\", \"dibayarkan_semula\": \"0\", \"sisa\": \"0\", \"ppk_nama\": \"Munawir Sajalai\", \"ppk_nip\": \"198712252020121001\"}', 'Selesai', 1, '2026-05-07 02:54:01', '2026-05-07 02:54:01');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `nama_lengkap` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT 'Pegawai',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `nama_lengkap`, `username`, `password`, `role`, `created_at`) VALUES
(1, 'Muhammad Alief', 'admin', 'admin123', 'Pegawai', '2026-05-04 14:58:03');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `surat`
--
ALTER TABLE `surat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `surat`
--
ALTER TABLE `surat`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `surat`
--
ALTER TABLE `surat`
  ADD CONSTRAINT `surat_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
