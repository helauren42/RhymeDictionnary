NAME = buildDb

SRCS = $(wildcard *.cpp)
OBJS = $(SRCS:.cpp=.o)
CFLAGS = -Wall -Werror -Wextra
FLAGMARIADB = -lmariadb
INCLUDE = -I/usr/include/mariadb

all: $(NAME)

$(NAME): $(OBJS)
	c++ $(INCLUDE) $(SRCS) $(FLAGMARIADB) -o $(NAME)

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all
