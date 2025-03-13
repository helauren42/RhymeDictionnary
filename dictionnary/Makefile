NAME = buildDb

SRCS = $(wildcard *.cpp)
OBJS = $(SRCS:.cpp=.o)
CFLAGS = -Wall -Werror -Wextra
FLAGMARIADB = -lmariadb
INCLUDE = -I/usr/include/mariadb

all: $(NAME)

$(NAME): $(OBJS)
	c++ $(INCLUDE) $(SRCS) -g3 $(FLAGMARIADB) -o $(NAME)
	clean

%.o: %.cpp
	c++ $(CFLAGS) $(INCLUDE) -g3 -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

run: all clean
	./buildDb

re: fclean all
