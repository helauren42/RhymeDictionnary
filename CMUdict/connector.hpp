#pragma once

#include <fstream>
#include <iostream>
#include <mariadb/mysql.h>
#include <vector>

#include "../MyCppLib/MyCppLib.hpp"
#include "../PATHS.hpp"
// #include "builder.hpp"

class Connector {
public:
  MYSQL *conn;
  MYSQL_ROW row;
  const std::string user;
  const std::string pwd;
  Connector() : user(fetchUser()), pwd(fetchPwd()) {
    connectToDb();
    initTable();
    Logger::winfo("Show tables:");
    makeQuery("SHOW TABLES");
  }
  ~Connector() {}
  // void addToken(const Token &token) {
  // }

private:
  void connectToDb() {
    conn = mysql_init(NULL);
    if (conn == NULL) {
      Logger::fatal("mysql_init() failed\n");
      return;
    }
    if (mysql_real_connect(conn, "localhost", user.c_str(), pwd.c_str(), "", 0,
                           NULL, 0) == NULL) {
      Logger::fatal("Failed to connect to db", mysql_error(conn));
      mysql_close(conn);
      return;
    }
    makeQuery("USE rd");
  }
  void initTable() {
    makeQuery(
        "CREATE TABLE IF NOT EXISTS dict(id INT AUTO_INCREMENT PRIMARY KEY, \
                word varchar(255) NOT NULL, \
                ipa TEXT NOT NULL, \
                syllables INT NOT NULL \
                )");
  }
  void makeQuery(const std::string &query) {
    Logger::info("make query: \"", query, "\"");
    if (mysql_query(conn, query.c_str())) {
      Logger::werror("Failed: ", mysql_error(conn));
      return;
    }
    MYSQL_RES *result = mysql_use_result(conn);
    if (!result) {
      Logger::werror("Could not retrieve result: ", mysql_error(conn));
      return;
    }
    while ((row = mysql_fetch_row(result)) != NULL) {
      Logger::winfo(row[0]);
    }
    mysql_free_result(result);
  }
  std::string fetchUser() {
    std::string secrets = PROJECT_DIR + std::string("secrets/secrets.txt");
    std::ifstream data(secrets);
    if (!data) {
      Logger::werror("Fetch user could not fetch data from: " + secrets);
      return nullptr;
    }
    std::string buffer;
    while (getline(data, buffer)) {
      if (buffer.find("DB_USER") != std::string::npos) {
        return split<std::vector>(buffer, "=")[1];
      }
    }
    Logger::werror("Fetch user could not fetch data from: " + secrets);
    return nullptr;
  }

  std::string fetchPwd() {
    std::string secrets = PROJECT_DIR + std::string("/dictionnary/secrets.txt");
    std::ifstream data(secrets);
    if (!data) {
      Logger::werror("Fetch pwd could not fetch data from: " + secrets);
      exit(1);
    }
    std::string buffer;
    while (getline(data, buffer)) {
      if (buffer.find("DB_PASSWORD") != std::string::npos) {
        return split<std::vector>(buffer, "=")[1];
      }
    }
    Logger::werror("Fetch pwd could not fetch data from: " + secrets);
    return nullptr;
  }
};
