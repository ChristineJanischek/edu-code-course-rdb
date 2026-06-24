<?php
declare(strict_types=1);

header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: SAMEORIGIN');
header('Referrer-Policy: no-referrer');
header('Cache-Control: no-store');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

$allowedMethods = ['GET', 'POST'];
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
if (!in_array($method, $allowedMethods, true)) {
    http_response_code(405);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['error' => 'Method not allowed'], JSON_UNESCAPED_UNICODE);
    exit;
}

$scriptName = $_SERVER['SCRIPT_NAME'] ?? '/api-proxy.php';
$requestUri = $_SERVER['REQUEST_URI'] ?? '/api-proxy.php';
$path = (string) parse_url($requestUri, PHP_URL_PATH);
$query = (string) parse_url($requestUri, PHP_URL_QUERY);

$forwardPath = '/';
if (str_starts_with($path, $scriptName)) {
    $forwardPath = substr($path, strlen($scriptName));
}
if ($forwardPath === '' || $forwardPath === false) {
    $forwardPath = '/';
}

if ($forwardPath === '/') {
    $forwardPath = '/api/v1/health';
}

if (!preg_match('#^/api/v1/[A-Za-z0-9_\-/]*$#', $forwardPath)) {
    http_response_code(400);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['error' => 'Invalid proxy path'], JSON_UNESCAPED_UNICODE);
    exit;
}

$internalBase = getenv('PYTHON_API_INTERNAL_URL') ?: 'http://python-api:8000';
$submissionApiKey = getenv('SUBMISSION_API_KEY') ?: '';

if ($submissionApiKey === '') {
    http_response_code(503);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['error' => 'Submission API key is not configured'], JSON_UNESCAPED_UNICODE);
    exit;
}

$targetUrl = rtrim($internalBase, '/') . $forwardPath;
if ($query !== '') {
    $targetUrl .= '?' . $query;
}

$headers = [
    'Accept: application/json',
    'Content-Type: application/json',
    'X-Internal-Api-Key: ' . $submissionApiKey,
];

$body = file_get_contents('php://input');
$context = stream_context_create([
    'http' => [
        'method' => $method,
        'header' => implode("\r\n", $headers),
        'content' => $body === false ? '' : $body,
        'ignore_errors' => true,
        'timeout' => 15,
    ],
]);

$responseBody = @file_get_contents($targetUrl, false, $context);
$upstreamHeaders = $http_response_header ?? [];
$statusCode = 502;
$contentType = 'application/json; charset=utf-8';
$traceId = null;

if (!empty($upstreamHeaders)) {
    if (preg_match('#\s(\d{3})\s#', $upstreamHeaders[0], $matches)) {
        $statusCode = (int) $matches[1];
    }

    foreach ($upstreamHeaders as $headerLine) {
        if (stripos($headerLine, 'Content-Type:') === 0) {
            $contentType = trim(substr($headerLine, strlen('Content-Type:')));
        }
        if (stripos($headerLine, 'X-Trace-Id:') === 0) {
            $traceId = trim(substr($headerLine, strlen('X-Trace-Id:')));
        }
    }
}

if ($responseBody === false) {
    $responseBody = json_encode(['error' => 'Upstream request failed'], JSON_UNESCAPED_UNICODE);
}

http_response_code($statusCode);
header('Content-Type: ' . $contentType);
if ($traceId) {
    header('X-Trace-Id: ' . $traceId);
}

echo $responseBody;
