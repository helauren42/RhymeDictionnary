NAME=buildDb

SRCS=$(wildcard *.cpp)
OBJS=$(SRCS:.cpp=.o)
CFLAGS=-Wall -Werror -Wextra

all: $(NAME)

$(NAME): $(OBJS)
	c++ -o $(NAME) $(OBJS)
	./$(NAME)

%.o: %.cpp
	c++ $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all
