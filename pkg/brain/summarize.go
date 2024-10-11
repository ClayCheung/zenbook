package brain

import (
	"context"
	"fmt"
	"os"

	"github.com/sashabaranov/go-openai"
	"github.com/zenmodel/zenmodel/processor"
)

func Summarize(bc processor.BrainContext) error {
	fmt.Println("Summarize assistant running...")

	query := bc.GetMemory("query").(string)
	result := bc.GetMemory("result").(string)

	

	prompt := []openai.ChatCompletionMessage{
		{
			Role: openai.ChatMessageRoleSystem,
			Content: `你是一个善于从多个帖子以及评论中总结内容的助手。帮助用户综合其他用户的评论了解查询的内容。返回 markdown 格式的内容。`,
		},
		{
			Role: openai.ChatMessageRoleUser,
			Content: fmt.Sprintf("根据下面内容总结关于 %s 信息。\n相关内容：%s\n", query, result),
		},
	}
	
	client := openai.NewClientWithConfig(openai.DefaultAzureConfig(os.Getenv("OPENAI_API_KEY"), os.Getenv("OPENAI_BASE_URL")))

	ctx := context.Background()
	resp, err := client.CreateChatCompletion(ctx,
		openai.ChatCompletionRequest{
			Model:    openai.GPT4o,
			Messages: append(prompt),
		},
	)
	if err != nil || len(resp.Choices) != 1 {
		return fmt.Errorf("Completion error: err:%v len(choices):%v\n", err,
			len(resp.Choices))
	}

	content := resp.Choices[0].Message.Content
	_ = bc.SetMemory("answer", content)

	return nil
}
