package brain

import (
	"github.com/zenmodel/zenmodel"
	"github.com/zenmodel/zenmodel/core"
	process "github.com/ClayCheung/zenbook/pkg/process"
)

func New () core.MultiLangBlueprint{
	bp := zenmodel.NewMultiLangBlueprint()


	neu1 := bp.AddNeuronWithPyProcessor("pkg/process", "xhsscraper", "XHSScraperProcessor", map[string]interface{}{
		"number": 3,
		"comments": 20,
		"replies": 50,
	})

	neu2 := bp.AddNeuron(process.Summarize)

	_, _ = bp.AddEntryLinkTo(neu1)
	_, _ = bp.AddLink(neu1, neu2)
	_, _ = bp.AddEndLinkFrom(neu2)

	return bp
}
