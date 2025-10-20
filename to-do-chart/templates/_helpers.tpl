{{- define "calculator.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "calculator.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end }}

{{- define "calculator.labels" -}}
app.kubernetes.io/name: {{ include "calculator.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: "{{ .Chart.AppVersion }}"
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "calculator.selectorLabels" -}}
app.kubernetes.io/name: {{ include "calculator.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
