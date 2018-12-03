SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `pwncoin` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `pwncoin`;

DROP TABLE IF EXISTS `gifts`;
CREATE TABLE `gifts` (
  `id` int(11) NOT NULL,
  `uid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `permissions`;
CREATE TABLE `permissions` (
  `r` tinyint(4) NOT NULL,
  `w` tinyint(4) NOT NULL,
  `table_name` varchar(255) NOT NULL,
  `role` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `permissions` (`r`, `w`, `table_name`, `role`) VALUES
(1, 1, 'users', 'guest'),
(1, 1, 'users', 'user'),
(1, 1, 'gifts', 'user'),
(1, 0, 'products', 'user');

DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `pid` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `filename` varchar(36) NOT NULL,
  `price` int(11) NOT NULL,
  `text` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `products` (`pid`, `name`, `filename`, `price`, `text`) VALUES
(2, 'The Twilight of the Idols - The Antichrist', 'bc7132d8fe84a14ae489ffba5b7ed86f.txt', 200, 'The Antichrist (German: Der Antichrist) is a book by the philosopher Friedrich Nietzsche, originally published in 1895. Although it was written in 1888, its controversial content made Franz Overbeck and Heinrich Köselitz delay its publication, along with Ecce Homo. (Wikipedia)'),
(3, 'The Flying Dutchman', 'a3ede5dc503a5bc78f4b657c1c47e770.txt', 300, 'The Flying Dutchman (German: Der fliegende Hollaender), WWV 63, is a German-language opera, with libretto and music by Richard Wagner.\r\n\r\nWagner claimed in his 1870 autobiography Mein Leben that he had been inspired to write the opera following a stormy sea crossing he made from Riga to London in July and August 1839.'),
(4, 'Faust; a Tragedy', '18006a86a502eca36aa01ca8a7bc0422.txt', 400, 'Faust is a tragic play in two parts by Johann Wolfgang von Goethe, usually known in English as Faust, Part One and Faust, Part Two. Although rarely staged in its entirety, it is the play with the largest audience numbers on German-language stages. Faust is considered by many to be Goethe\'s magnum opus and the greatest work of German literature. (Wikipedia)'),
(5, 'This Software', '45d47fe4f1ed9d801fe528e27b343249.zip', 600, 'Get the amazing software we build for \r\nthis beautiful website. Including our\r\nblockchain implementation and SQL abstraction layer. Featuring the latest technologies.'),
(6, 'Flaggy McFlagerson and Her Flag', '8b7220fa65f65450a18cbba6148d58c0.txt', 10000000, 'Exclusively here!! The first novel of Peter Flag, describing a young womans journey to her flag. This book touches everyone with its detailed description of the flag!');

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `uid` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `transactions` text NOT NULL,
  `password` varchar(40) NOT NULL,
  `tags` text NOT NULL,
  `got_gift` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `gifts`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `products`
  ADD PRIMARY KEY (`pid`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`uid`),
  ADD UNIQUE KEY `name` (`name`);


ALTER TABLE `gifts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

ALTER TABLE `products`
  MODIFY `pid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

ALTER TABLE `users`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

CREATE USER 'pwncoin'@'%'  IDENTIFIED BY 'Ahd92uaj99ADAD';
GRANT ALL PRIVILEGES ON pwncoin.* To 'pwncoin'@'%';
